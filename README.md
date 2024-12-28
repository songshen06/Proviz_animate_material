## Shader Animation Setup - User Interface Guide

This section covers the interface elements available in the shader animation plugin. It allows users to configure various settings for the rendering and animation process.

### 1. Render Resolution

- **Description**: This section defines the resolution of the rendered images.
- **Inputs**:
  - **Width**: The width of the rendered image (default is 3840).
  - **Height**: The height of the rendered image (default is 2160).

---

### 2. Shader Path

- **Description**: Specifies the path to the shader you want to apply to the texture.
- **Input**: Enter the shader path (e.g., `/World/Looks/MyShader`).

---

### 3. Animation Folder Path

- **Description**: Path to the folder containing the animation textures.
- **Input**: Enter the folder path where the animation textures are stored.

---

### 4. Start Time Code

- **Description**: Specifies the time code at which the animation should begin.
- **Input**: Enter the start time code (default is 0).

---

### 5. Frame Duration

- **Description**: Defines the number of frames each texture will be displayed before transitioning to the next texture in the sequence.
- **Input**: Enter the frame duration (default is 6).

---

### 6. Wait Time Between Textures

- **Description**: Sets the wait time in seconds between each texture frame during the animation.
- **Input**: Enter the wait time (default is 0.5 seconds).

---

### 7. Output Directory

- **Description**: Specifies the directory where rendered images will be saved.
- **Input**: Enter the output directory path (default is `/path/to/output`).

---

### 8. Output File Name Prefix

- **Description**: Defines the prefix to be used for the output image file names.
- **Input**: Enter the prefix (default is `frame`).

---

### 9. Select Texture Type

- **Description**: Choose the texture type to be applied to the shader.
- **Options**:
  - **Opacity Texture**: Select for opacity textures.
  - **Diffuse Texture**: Select for diffuse textures.

---

### 10. Buttons

The following buttons control the core functionality of the plugin:

#### 10.1 **Run Animation**

- **Description**: Starts the animation rendering process.
- **Action**: Click the `Run Animation` button to begin the rendering of the textures in sequence. The frame duration and wait time between textures will dictate the pace of the animation.

#### 10.2 **Clear Animation**

- **Description**: Clears the current animation settings and resets the texture configuration.
- **Action**: Click the `Clear Animation` button to reset the animation settings and start fresh.

#### 10.3 **Terminate**

- **Description**: Terminates the ongoing rendering or animation process.
- **Action**: Click the `Terminate` button to immediately stop the current animation rendering.

#### 10.4 **Clear Inputs**

- **Description**: Clears all the input fields, allowing you to reset the configuration.
- **Action**: Click the `Clear Inputs` button to reset all settings to their default values.

---

### Example Usage Flow

1. **Set Input Parameters**

   - Define your render resolution, shader path, animation folder, and other settings in the fields.

2. **Run Animation**

   - Once the settings are configured, click the `Run Animation` button to start rendering the textures based on the animation setup.

3. **Clear Animation**

   - To clear the current animation and settings, click the `Clear Animation` button.

4. **Terminate**

   - To stop the ongoing rendering or animation process at any time, click the `Terminate` button.

5. **Clear Inputs**
   - To reset all input fields to their default values, click the `Clear Inputs` button.
