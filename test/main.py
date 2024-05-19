import cv2
import json
import numpy as np

# Define spots polygons
spots = {
    'Spot1': [(95, 343), (185, 312), (251, 337), (159, 387)],
    'Spot2': [(488, 395), (658, 432), (598, 474), (420, 420)],
    'Spot3': [(393, 418), (591, 478), (518, 523), (347, 437)],
    'Spot4': [(417, 581), (510, 536), (319, 449), (265, 466)],
    'Spot5': [(246, 662), (96, 508), (200, 468), (400, 588)]
}

# Open and read the JSON data file
with open("data.txt", "r") as file:
    for line in file:
        # Replace single quotes with double quotes
        line = line.replace("'", "\"")
        # Parse JSON data from the line
        json_data = json.loads(line.strip())

        # Extract bounding box coordinates for the "car" class
        car_bboxes = json_data['BBoxes_xyxy'].get('car', [])

        image = cv2.imread("Full_Camera_2024_05_16_10PM_21_13.jpeg")

        # Initialize inside_spot for each spot to False
        inside_spot = {spot: False for spot in spots.keys()}
        
        # Draw bounding boxes for the "car" class on the image
        for i in range(0, len(car_bboxes), 4):
            x_min, y_min, x_max, y_max = map(int, car_bboxes[i:i+4])

            # Draw bounding box
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Calculate midpoint
            midpoint = ((x_min + x_max) // 2, (y_min + y_max) // 2)

            # Draw midpoint as red point
            cv2.circle(image, midpoint, 5, (0, 0, 255), -1)

            # Check if midpoint is inside any spot polygon
            for spot, polygon in spots.items():
                # Create a mask for the spot polygon
                mask = np.zeros_like(image)
                cv2.fillPoly(mask, [np.array(polygon)], color=(255, 255, 255))
                # Check if the midpoint falls within the filled area
                if mask[midpoint[1], midpoint[0], 0] == 255:
                    inside_spot[spot] = True

        # Draw spots polygons with appropriate color
        for spot, polygon in spots.items():
            color = (0, 0, 255) if inside_spot[spot] else (255, 255, 255)
            cv2.polylines(image, [np.array(polygon)], isClosed=True, color=color, thickness=2)

        # Display the image with bounding boxes and spots
        cv2.imshow("Image with Car Bounding Boxes and Spots", image)
        cv2.waitKey(0)  # Wait for any key press to continue

# Close all OpenCV windows
cv2.destroyAllWindows()

