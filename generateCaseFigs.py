from paraview.simple import *
import os
import subprocess

paraview.simple._DisableFirstRenderCameraReset()

# Directory containing all case folders
base_dir = "."
output_dir = "figs"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# List all case folders (e.g., ["case0001", "case0002", ...])
case_folders = sorted([f for f in os.listdir(base_dir) if f.startswith("case")])
#case_folders = ["case0001"] #Outcomment to test on a single case

for case in case_folders:
    case_path = os.path.join(base_dir, case)
    case_num = case[4:]  # Extract "0001" from "case0001"
    output_image = os.path.join(output_dir, f"{case_num}.png")
    # Strip .png if present in output_image
    output_base = output_image[:-4] if output_image.endswith('.png') else output_image

    print(f"Processing {case}...")

    # Load OpenFOAM data
    foam_reader = OpenFOAMReader(FileName=os.path.join(case_path, "case.foam"))
    foam_reader.UpdatePipeline()

    # Go to last time step
    animationScene1 = GetAnimationScene()
    animationScene1.GoToLast()

    # Colour domain by magnitude of U cell values
    renderView1 = GetActiveViewOrCreate('RenderView')
    casefoamDisplay = Show(foam_reader, renderView1)

    fields = [
        ('U', 'Magnitude', 'mag(U)'),  # (array_name, component, legend title)
        ('p', '', 'p'),
        ('T', '', 'T'),
    ]

    for field_name, component, legend_title in fields:
        # Color by field (with or without magnitude)
        if component == 'Magnitude':
            ColorBy(casefoamDisplay, ('CELLS', field_name, 'Magnitude'))
        else:
            ColorBy(casefoamDisplay, ('CELLS', field_name))

        # Get and rescale the color transfer function
        lut = GetColorTransferFunction(field_name)
        lut.RescaleTransferFunctionToDataRange(True)

        # Configure the scalar bar (color legend)
        color_bar = GetScalarBar(lut, renderView1)
        color_bar.WindowLocation = 'Any Location'
        color_bar.Position = [0.9, 0.2]
        color_bar.ScalarBarLength = 0.6
        color_bar.AutoOrient = 0
        color_bar.Orientation = 'Vertical'
        color_bar.Title = legend_title
        color_bar.ComponentTitle = ''
        color_bar.TitleColor = [0.0, 0.0, 0.0]
        color_bar.LabelColor = [0.0, 0.0, 0.0]
        color_bar.Visibility = 1

        # 🧭 Set consistent camera/view/background settings
        renderView1.InteractionMode = '2D'
        renderView1.CameraPosition = [0.025, 0, 2]
        renderView1.CameraFocalPoint = [0.025, 0, 0]
        renderView1.CameraParallelProjection = 1
        renderView1.CameraParallelScale = 0.01
        renderView1.ViewSize = [1200, 150]
        SetViewProperties(
            Background=[1, 1, 1],
            UseColorPaletteForBackground=0,
        )

        # 🔄 Force render to apply all settings
        Render()

        # Save screenshot for this field
        output_file = f"{output_base}_{field_name}.png"
        SaveScreenshot(output_file, renderView1,
            FontScaling='Do not scale fonts',
            OverrideColorPalette='',
            StereoMode='No change',
            TransparentBackground=0
        )

        # hide scalar bar for next field (optional cleanup)
        color_bar.Visibility = 0

    # Concatenate images vertically
    input_images = [f"{output_base}_{field[0]}.png" for field in fields]
    subprocess.run(['convert', '-append'] + input_images + [output_image], check=True)
    subprocess.run(['rm', '-f'] + input_images, check=True)

    # Clean up (avoid memory buildup)
    Delete(foam_reader)
    Delete(casefoamDisplay)
    del foam_reader, casefoamDisplay

print("All cases processed!")
