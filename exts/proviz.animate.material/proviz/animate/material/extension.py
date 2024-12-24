import omni.ext
import omni.ui as ui
import asyncio
from pxr import Usd, UsdShade, Sdf
from glob import glob
import os

# UI Module

class ShaderAnimationUI:
    def __init__(self, on_run_animation, on_clear_animation, on_clear_inputs):
        self.window = ui.Window("Shader Animation Setup", width=400, height=550)
        self.on_run_animation = on_run_animation
        self.on_clear_animation = on_clear_animation
        self.on_clear_inputs = on_clear_inputs
        self._build_ui()

    def _build_ui(self):
        # Resolve icon paths dynamically
        icons_path = os.path.join(os.path.dirname(__file__), "icons")
        radio_off_icon = f"{icons_path}/radio_off.svg"
        radio_on_icon = f"{icons_path}/radio_on.svg"

        # Print resolved paths for debugging
        print(f"Radio Off Icon Path: {radio_off_icon}")
        print(f"Radio On Icon Path: {radio_on_icon}")

        with self.window.frame:
            with ui.VStack(spacing=10):
                # Shader Path input
                ui.Label("Shader Path:(eg./World/Looks/TCCW/Shader)", height=20)
                self.shader_path_field = ui.StringField(height=30)

                # Animation Folder Path input
                ui.Label("Animation Folder Path:", height=20)
                self.animation_folder_field = ui.StringField(height=30)

                # Animation Start Time Code
                ui.Label("Start Time Code:", height=20)
                self.start_time_code_field = ui.IntField(
                    height=30, tooltip="Enter the starting time code for the animation."
                )
                self.start_time_code_field.model.set_value(0)

                # Frame Duration input
                ui.Label("Frame Duration (frames per texture):", height=20)
                self.frame_duration_field = ui.IntField(
                    height=30, tooltip="Enter the number of frames each texture should hold."
                )
                self.frame_duration_field.model.set_value(2)  # Default to 2 frames per texture

                # Texture Input using RadioCollection with custom style
                ui.Label("Texture Input (e.g., opacity_texture):", height=20)
                self.texture_options = [
                    "opacity_texture",
                    "diffuse_texture",
                    "normal_texture",
                    "specular_texture",
                ]
                self.texture_collection = ui.RadioCollection()

                # Define custom style for RadioButton
                radio_button_style = {
                    "background_color": ui.color(0, 0, 0, 0),  # Transparent background
                    "image_url": radio_off_icon,  # Custom "unchecked" icon
                    ":checked": {"image_url": radio_on_icon},  # Custom "checked" icon
                }

                for index, option in enumerate(self.texture_options):
                    with ui.HStack(spacing=5, height=30):
                        ui.RadioButton(
                            radio_collection=self.texture_collection,
                            width=30,
                            height=30,
                            style=radio_button_style,
                        )
                        ui.Label(option, name="text", height=30)

                # Buttons for user actions
                with ui.HStack(spacing=10):
                    # Run Animation Button
                    self.run_button = ui.Button("Run Animation", height=30)
                    self.run_button.set_clicked_fn(self.on_run_animation)

                    # Clear Animation Button
                    self.clear_animation_button = ui.Button("Clear Animation", height=30)
                    self.clear_animation_button.set_clicked_fn(self.on_clear_animation)

                    # Clear Inputs Button
                    self.clear_button = ui.Button("Clear Inputs", height=30)
                    self.clear_button.set_clicked_fn(self.on_clear_inputs)

    def get_inputs(self):
        return {
            "shader_path": self.shader_path_field.model.get_value_as_string().strip(),
            "animation_folder": self.animation_folder_field.model.get_value_as_string().strip(),
            "texture_input_name": self.texture_options[
                self.texture_collection.model.as_int
            ],  # Get selected texture name
            "start_time_code": self.start_time_code_field.model.get_value_as_int(),
            "frame_duration": self.frame_duration_field.model.get_value_as_int(),
        }

    def clear_inputs(self):
        self.shader_path_field.model.set_value("")
        self.animation_folder_field.model.set_value("")
        self.texture_collection.model.set_value(0)  # Reset to the first option
        self.start_time_code_field.model.set_value(0)
        self.frame_duration_field.model.set_value(2)


    def get_inputs(self):
        return {
            "shader_path": self.shader_path_field.model.get_value_as_string().strip(),
            "animation_folder": self.animation_folder_field.model.get_value_as_string().strip(),
            "texture_input_name": self.texture_options[self.texture_collection.model.as_int],  # Get selected texture name
            "start_time_code": self.start_time_code_field.model.get_value_as_int(),
            "frame_duration": self.frame_duration_field.model.get_value_as_int()
        }

    def clear_inputs(self):
        self.shader_path_field.model.set_value("")
        self.animation_folder_field.model.set_value("")
        self.texture_collection.model.set_value(0)  # Reset to the first option
        self.start_time_code_field.model.set_value(0)
        self.frame_duration_field.model.set_value(2)





# Animation Logic Module
class ShaderAnimationLogic:
    @staticmethod
    async def start_animation(stage, shader_path, animation_folder, texture_input_name, start_time_code, frame_duration):
        try:
            print(f"[ShaderAnimationLogic] Starting animation setup...")
            print(f"[ShaderAnimationLogic] Shader Path: {shader_path}")
            print(f"[ShaderAnimationLogic] Animation Folder Absolute Path: {animation_folder}")
            print(f"[ShaderAnimationLogic] Using Texture Input: {texture_input_name}")
            print(f"[ShaderAnimationLogic] Start Time Code: {start_time_code}")
            print(f"[ShaderAnimationLogic] Frame Duration: {frame_duration}")

            # Find the Shader using UsdShade API
            shader_prim = stage.GetPrimAtPath(shader_path)
            if not shader_prim.IsValid():
                print(f"[ShaderAnimationLogic] Shader not found at path: {shader_path}")
                return

            shader = UsdShade.Shader(shader_prim)
            texture_input = shader.GetInput(texture_input_name)
            if not texture_input:
                print(f"[ShaderAnimationLogic] Input '{texture_input_name}' not found in shader.")
                return

            valid_files = ShaderAnimationLogic._get_valid_files(animation_folder)
            if not valid_files:
                print("[ShaderAnimationLogic] No valid images found in the provided folder.")
                return

            print(f"[ShaderAnimationLogic] Found {len(valid_files)} valid image files.")

            # Assign texture sequence with adjusted timeline
            for i, file in enumerate(valid_files):
                for j in range(frame_duration):
                    time_code = start_time_code + i * frame_duration + j
                    texture_input.Set(Sdf.AssetPath(file), Usd.TimeCode(time_code))
                    print(f"[ShaderAnimationLogic] Set texture frame {time_code}: {file}")

            # Adjust timeline
            end_time_code = start_time_code + len(valid_files) * frame_duration
            stage.SetStartTimeCode(start_time_code)
            stage.SetEndTimeCode(end_time_code - 1)
            print(f"[ShaderAnimationLogic] Timeline adjusted: Start={start_time_code}, End={end_time_code - 1}")

        except Exception as e:
            print(f"[ShaderAnimationLogic] Error: {e}")

    @staticmethod
    def clear_animation(stage, shader_path, texture_input_name):
        try:
            shader_prim = stage.GetPrimAtPath(shader_path)
            if not shader_prim.IsValid():
                print(f"[ShaderAnimationLogic] Shader not found at path: {shader_path}")
                return

            shader = UsdShade.Shader(shader_prim)
            texture_input = shader.GetInput(texture_input_name)
            if not texture_input:
                print(f"[ShaderAnimationLogic] Input '{texture_input_name}' not found in shader.")
                return

            texture_input.GetAttr().Clear()
            stage.SetStartTimeCode(0)
            stage.SetEndTimeCode(0)
            print("[ShaderAnimationLogic] Animation cleared successfully.")

        except Exception as e:
            print(f"[ShaderAnimationLogic] Error: {e}")

    @staticmethod
    def _get_valid_files(folder):
        files = sorted(glob(os.path.join(folder, "*")))
        return [f for f in files if os.path.isfile(f) and f.lower().endswith((".jpg", ".png"))]

# Main Extension
class ShaderAnimationExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[ShaderAnimationExtension] Plugin Started")
        self.ext_id = ext_id

        self.ui = ShaderAnimationUI(
            on_run_animation=self._run_animation,
            on_clear_animation=self._clear_animation,
            on_clear_inputs=self._clear_inputs
        )

    def on_shutdown(self):
        print("[ShaderAnimationExtension] Plugin Shutdown")
        if self.ui.window:
            self.ui.window.destroy()
            self.ui = None

    def _run_animation(self):
        inputs = self.ui.get_inputs()
        if not inputs["shader_path"] or not inputs["animation_folder"] or not inputs["texture_input_name"]:
            print("[ShaderAnimationExtension] Please provide shader path, animation folder, and texture input.")
            return

        if inputs["frame_duration"] <= 0:
            print("[ShaderAnimationExtension] Frame duration must be greater than 0.")
            return

        stage = omni.usd.get_context().get_stage()
        asyncio.ensure_future(ShaderAnimationLogic.start_animation(
            stage,
            inputs["shader_path"],
            inputs["animation_folder"],
            inputs["texture_input_name"],
            inputs["start_time_code"],
            inputs["frame_duration"]
        ))

    def _clear_animation(self):
        inputs = self.ui.get_inputs()
        if not inputs["shader_path"] or not inputs["texture_input_name"]:
            print("[ShaderAnimationExtension] Please provide shader path and texture input to clear the animation.")
            return

        stage = omni.usd.get_context().get_stage()
        ShaderAnimationLogic.clear_animation(
            stage,
            inputs["shader_path"],
            inputs["texture_input_name"]
        )

    def _clear_inputs(self):
        self.ui.clear_inputs()

