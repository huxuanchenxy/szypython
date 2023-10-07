from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# Convert SVG to ReportLab Graphics object
drawing = svg2rlg('robot.svg')

# Render the Graphics object to PNG
renderPM.drawToFile(drawing, 'output.png', fmt='PNG')