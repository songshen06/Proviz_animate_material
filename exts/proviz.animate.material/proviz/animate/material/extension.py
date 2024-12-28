import omni.ext
import omni.ui as ui
import asyncio
from pxr import Usd, UsdShade, Sdf
from omni.kit.viewport.utility import get_active_viewport_window
from omni.kit.widget.viewport.capture import FileCapture
import os
from glob import glob
import omni.timeline

class ShaderAnimationUI:
    def __init__(self, on_run_animation, on_clear_inputs, on_clear_animation, on_terminate_process):
        self.window = ui.Window("Render and Animation Setup", width=400, height=900)
        self.on_run_animation = on_run_animation
        self.on_clear_inputs = on_clear_inputs
        self.on_clear_animation = on_clear_animation
        self.on_terminate_process = on_terminate_process
        self._build_ui()

    def _build_ui(self):
        with self.window.frame:
            with ui.VStack(spacing=10):
                # Render Resolution
                ui.Label("Render Resolution (Width x Height):", height=20)
                self.resolution_width = ui.IntField(height=30)
                self.resolution_width.model.set_value(3840)
                self.resolution_height = ui.IntField(height=30)
                self.resolution_height.model.set_value(2160)

                # Animation Setup
                ui.Label("Shader Path (e.g., /World/Looks/MyShader):", height=20)
                self.shader_path_field = ui.StringField(height=30)

                ui.Label("Animation Folder Path:", height=20)
                self.animation_folder_field = ui.StringField(height=30)

                ui.Label("Start Time Code:", height=20)
                self.start_time_code_field = ui.IntField(height=30)
                self.start_time_code_field.model.set_value(0)

                ui.Label("Frame Duration (frames per texture):", height=20)
                self.frame_duration_field = ui.IntField(height=30)
                self.frame_duration_field.model.set_value(6)

                ui.Label("Wait Time Between Textures (seconds):", height=20)
                self.wait_time_field = ui.FloatField(height=30)
                self.wait_time_field.model.set_value(0.5)

                ui.Label("Output Directory (for rendered images):", height=20)
                self.output_dir_field = ui.StringField(height=30)
                self.output_dir_field.model.set_value("/path/to/output")

                ui.Label("Output File Name Prefix:", height=20)
                self.output_prefix_field = ui.StringField(height=30)
                self.output_prefix_field.model.set_value("frame")

                # Select Texture Type
                ui.Label("Select Texture Type:", height=20)
                self.texture_type_collection = ui.RadioCollection()

                with ui.HStack(spacing=5, height=30):
                    ui.RadioButton(
                        radio_collection=self.texture_type_collection,
                        text="Opacity Texture",
                        width=120,
                        height=30
                    )
                    ui.RadioButton(
                        radio_collection=self.texture_type_collection,
                        text="Diffuse Texture",
                        width=120,
                        height=30
                    )

                # Buttons
                with ui.HStack(spacing=10):
                    self.run_button = ui.Button("Run Animation", height=30)
                    self.run_button.set_clicked_fn(self.on_run_animation)

                    self.clear_animation_button = ui.Button("Clear Animation", height=30)
                    self.clear_animation_button.set_clicked_fn(self.on_clear_animation)

                    self.terminate_button = ui.Button("Terminate", height=30)
                    self.terminate_button.set_clicked_fn(self.on_terminate_process)

                    self.clear_button = ui.Button("Clear Inputs", height=30)
                    self.clear_button.set_clicked_fn(self.on_clear_inputs)

    def get_inputs(self):
        return {
            "resolution_width": self.resolution_width.model.get_value_as_int(),
            "resolution_height": self.resolution_height.model.get_value_as_int(),
            "shader_path": self.shader_path_field.model.get_value_as_string().strip(),
            "animation_folder": self.animation_folder_field.model.get_value_as_string().strip(),
            "start_time_code": self.start_time_code_field.model.get_value_as_int(),
            "frame_duration": self.frame_duration_field.model.get_value_as_int(),
            "wait_time": self.wait_time_field.model.get_value_as_float(),
            "output_dir": self.output_dir_field.model.get_value_as_string().strip(),
            "output_prefix": self.output_prefix_field.model.get_value_as_string().strip(),
            "texture_type": "opacity_texture" if self.texture_type_collection.model.as_int == 0 else "diffuse_texture",
        }

    def clear_inputs(self):
        self.resolution_width.model.set_value(1920)
        self.resolution_height.model.set_value(1080)
        self.shader_path_field.model.set_value("")
        self.animation_folder_field.model.set_value("")
        self.start_time_code_field.model.set_value(0)
        self.frame_duration_field.model.set_value(6)
        self.wait_time_field.model.set_value(0.5)
        self.output_dir_field.model.set_value("/path/to/output")
        self.output_prefix_field.model.set_value("frame")
        self.texture_type_collection.model.set_value(0)
    
    


class ShaderAnimationLogic:
    terminate_flag = False

    @staticmethod
    async def render_frame(output_path, resolution):
        """
        Render a single frame using the active ViewportAPI and save to file.
        """
        viewport_window = get_active_viewport_window()
        if not viewport_window:
            print("Error: No active viewport found.")
            return

        viewport_api = viewport_window.viewport_api
        viewport_api.fill_frame = False  # Disable auto resolution adjustment
        viewport_api.resolution = resolution
        print(f"Resolution set to: {viewport_api.resolution}")

        capture = viewport_api.schedule_capture(FileCapture(output_path))
        captured_aovs = await capture.wait_for_result()

        if captured_aovs:
            print(f'Image was successfully saved to "{output_path}"')
        else:
            print("Failed to save the image.")



    @staticmethod
    async def run_animation(inputs):
        stage = omni.usd.get_context().get_stage()
        shader_path = inputs["shader_path"]
        animation_folder = inputs["animation_folder"]
        resolution = (inputs["resolution_width"], inputs["resolution_height"])
        frame_duration = inputs["frame_duration"]
        wait_time = inputs["wait_time"]
        output_dir = inputs["output_dir"]
        output_prefix = inputs["output_prefix"]
        texture_type = inputs["texture_type"]

        # Validate shader and input
        shader_prim = stage.GetPrimAtPath(shader_path)
        if not shader_prim.IsValid():
            print(f"Error: Shader not found at path {shader_path}")
            return

        shader = UsdShade.Shader(shader_prim)
        texture_input = shader.GetInput(texture_type)
        if not texture_input:
            print(f"Error: Specified texture input '{texture_type}' not found in Shader.")
            return

        # Validate animation folder and output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        # Load valid texture files
        files = sorted(glob(os.path.join(animation_folder, "*")))
        valid_files = [f for f in files if os.path.isfile(f) and f.lower().endswith((".jpg", ".png"))]
        if not valid_files:
            print("Error: No valid texture files found.")
            return

        ShaderAnimationLogic.terminate_flag = False

        # Get the active viewport
        viewport_window = get_active_viewport_window()
        if not viewport_window:
            print("Error: No active viewport found.")
            return

        viewport_api = viewport_window.viewport_api

        # Get the Omni Timeline interface
        timeline = omni.timeline.get_timeline_interface()

        # Set start and end times for the timeline
        start_time_code = 0
        end_time_code = len(valid_files) * frame_duration
        timeline.set_start_time(start_time_code)
        timeline.set_end_time(end_time_code)

        for texture_index, texture_path in enumerate(valid_files):
            if ShaderAnimationLogic.terminate_flag:
                print("Rendering process terminated by user.")
                break

            try:
                # Step 1: Load the texture
                texture_input.Set(Sdf.AssetPath(texture_path))
                print(f"Assigned texture '{texture_path}' to {texture_type}")

                # Step 2: Set the current time on the timeline
                frame_start_time = texture_index * frame_duration
                timeline.set_current_time(frame_start_time)
                print(f"Set timeline current time to {frame_start_time} for texture {texture_path}")

                # Step 3: Wait for Shader and Viewport to update
                print("Waiting for render settings change...")
                await viewport_api.wait_for_render_settings_change()
                print("Render settings updated.")

                print("Waiting for rendered frame to be completed...")
                await viewport_api.wait_for_rendered_frames(1)
                print("Rendered frame completed.")

                # Step 4: Render multiple frames for the current texture
                for frame_offset in range(frame_duration):
                    frame_index = frame_start_time + frame_offset
                    output_path = os.path.join(output_dir, f"{output_prefix}_{frame_index:04d}.png")
                    print(f"Rendering frame {frame_index} for texture '{texture_path}'")

                    # Capture the current frame
                    capture = viewport_api.schedule_capture(FileCapture(output_path))
                    await capture.wait_for_result()

                    # Add a short wait to ensure rendering stability
                    await asyncio.sleep(wait_time)

            except Exception as e:
                print(f"Error during texture {texture_index}: {e}")

        print("Animation rendering completed.")


    
    @staticmethod
    def clear_animation(shader_path, texture_type):
        """
        Clear the animation applied to the specified Shader.

        Args:
            shader_path (str): Path to the Shader in the USD Stage.
            texture_type (str): The type of texture input to clear (e.g., "opacity_texture").
        """
        stage = omni.usd.get_context().get_stage()

        # Validate the Shader path
        shader_prim = stage.GetPrimAtPath(shader_path)
        if not shader_prim.IsValid():
            print(f"Error: Shader not found at path {shader_path}")
            return

        shader = UsdShade.Shader(shader_prim)
        texture_input = shader.GetInput(texture_type)
        if not texture_input:
            print(f"Error: Specified texture input '{texture_type}' not found in Shader.")
            return

        try:
            # Clear the texture input
            texture_input.GetAttr().Clear()

            # Reset the Timeline to the initial state
            timeline = omni.timeline.get_timeline_interface()
            timeline.set_current_time(0)
            timeline.stop()  # Ensure the timeline is stopped after resetting time

            print(f"Cleared animation for Shader at {shader_path}, texture type: {texture_type}")
        except Exception as e:
            print(f"Error clearing animation: {e}")



    @staticmethod
    def terminate_process():
        ShaderAnimationLogic.terminate_flag = True


class ShaderAnimationExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("Shader Animation Extension Started")
        self.ext_id = ext_id
        self.ui = ShaderAnimationUI(
            on_run_animation=self._run_animation,
            on_clear_inputs=self._clear_inputs,
            on_clear_animation=self._clear_animation,
            on_terminate_process=self._terminate_process,
        )

    def on_shutdown(self):
        print("Shader Animation Extension Shutdown")
        if self.ui.window:
            self.ui.window.destroy()
            self.ui = None

    def _run_animation(self):
        inputs = self.ui.get_inputs()
        asyncio.ensure_future(ShaderAnimationLogic.run_animation(inputs))

    def _clear_inputs(self):
        self.ui.clear_inputs()

    def _clear_animation(self):
        inputs = self.ui.get_inputs()
        ShaderAnimationLogic.clear_animation(inputs["shader_path"], inputs["texture_type"])

    def _terminate_process(self):
        ShaderAnimationLogic.terminate_process()
