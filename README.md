# Shader Animation Extension Documentation

## Overview

The Shader Animation Extension is a custom Omniverse plugin designed to apply and manage texture-based animation sequences on shader inputs. It provides an easy-to-use UI for configuring animation parameters, such as shader path, texture input, animation folder, and frame duration.

![Watch the video](https://github.com/songshen06/Proviz_animate_material/blob/master/animate_texture.mp4)

## Features

### Run Animation

- Allows the user to specify a shader path and apply a texture sequence as an animation.
- Supports custom frame durations for each texture.
- Automatically adjusts the USD timeline based on the provided configuration.

### Clear Animation

- Removes the animation configuration from the shader input.
- Resets the timeline to default values.

### Clear Inputs

- Resets all UI fields to their default values.

## User Interface

### Inputs

#### Shader Path

- Specify the USD path of the shader where the animation will be applied.
- Example: `/World/Looks/Shader1`.

#### Texture Input

- Specify the shader's texture input to which the animation will be applied.
- Example: `opacity_texture`.

#### Animation Folder Path

- Specify the folder containing the texture files to use for the animation.
- Only `.jpg` and `.png` formats are supported.

#### Start Time Code

- Set the time code where the animation begins.
- Example: `0`.

#### Frame Duration

- Define how many frames each texture will be displayed.
- Example: `2` (each texture will last for 2 frames).

### Buttons

#### Run Animation

- Applies the texture sequence as an animation to the specified shader.
- Dynamically calculates the timeline's end based on the number of textures and frame duration.

#### Clear Animation

- Removes the texture sequence animation and resets the timeline.

#### Clear Inputs

- Resets all fields in the UI to their default values.

## Workflow

1. Open the extension.
2. Fill in the required fields:
   - **Shader Path**: Enter the path to the shader.
   - **Texture Input**: Specify the shader input name (e.g., `opacity_texture`).
   - **Animation Folder Path**: Provide the folder containing texture sequence files.
   - **Start Time Code**: Set the animation's starting time code.
   - **Frame Duration**: Specify the number of frames each texture will last.
3. Click **Run Animation** to apply the animation.
4. To remove the animation, click **Clear Animation**.
5. Use **Clear Inputs** to reset the form for a new configuration.

## Error Handling

### Invalid Shader Path

- Ensure the specified shader path exists in the USD stage.
- Error Message: `Shader not found at path: <path>`.

### Invalid Texture Input

- Ensure the specified texture input exists on the shader.
- Error Message: `Input '<texture_input>' not found in shader`.

### Empty or Missing Animation Folder

- Ensure the folder contains valid `.jpg` or `.png` files.
- Error Message: `No valid images found in the provided folder`.

### Frame Duration Error

- Ensure frame duration is greater than `0`.
- Error Message: `Frame duration must be greater than 0`.

## Development Details

### Code Structure

The plugin is modularized into the following components:

#### UI Module

- Handles the creation of user interface elements and captures user inputs.

#### Animation Logic Module

- Contains methods for applying and clearing animations.
- Includes helper functions for file validation and timeline adjustments.

#### Main Extension

- Manages the plugin's lifecycle and bridges the UI with the animation logic.

### Key Functions

#### UI Module

- `get_inputs()`: Retrieves user input values from the UI fields.
- `clear_inputs()`: Resets all input fields to default values.

#### Animation Logic Module

- `start_animation()`:
  - Applies the texture sequence animation to the specified shader input.
  - Adjusts the timeline dynamically based on textures and frame duration.
- `clear_animation()`:
  - Removes the animation configuration and resets the timeline.
- `_get_valid_files()`:
  - Filters valid texture files (`.jpg`, `.png`) from the provided folder.

#### Main Extension

- `_run_animation()`: Retrieves user inputs and triggers the animation logic.
- `_clear_animation()`: Clears the animation using the animation logic.
- `_clear_inputs()`: Resets the UI fields.

## Extensibility

### To add support for more texture formats:

- Update the `_get_valid_files()` method in `ShaderAnimationLogic`.

### To enhance UI capabilities:

- Add new input fields or dropdowns in the `ShaderAnimationUI` class.

## Example

### Configuration

- **Shader Path**: `/World/Looks/MyShader`
- **Texture Input**: `diffuse_texture`
- **Animation Folder Path**: `/path/to/textures`
- **Start Time Code**: `0`
- **Frame Duration**: `2`

### Result

- Each texture from the folder is applied for 2 frames.
- Timeline is adjusted to fit all textures.

## Future Improvements

- **Preview Mode**: Add functionality to preview animations before applying.
- **Batch Processing**: Enable applying animations to multiple shaders simultaneously.
- **Enhanced Error Reporting**: Provide detailed error messages and suggestions for resolving issues.

## Conclusion

This plugin simplifies the process of applying texture-based animations to shaders in Omniverse. Its modular design ensures ease of maintenance and scalability for future enhancements.
