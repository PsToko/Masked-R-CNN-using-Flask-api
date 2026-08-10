import matplotlib.pyplot as plt


def draw_predictions(image, results, output_path):
    """
    Draw bounding boxes, labels and segmentation masks
    on an image and save the result.
    """

    plt.figure(figsize=(12, 8))

    plt.imshow(image)

    for result in results:

        box = result["box"]
        class_name = result["class_name"]
        confidence = result["confidence"]
        mask = result["mask"]

        x1, y1, x2, y2 = box

        # Bounding box
        rectangle = plt.Rectangle(
            (x1, y1),
            x2 - x1,
            y2 - y1,
            fill=False,
            linewidth=2
        )

        plt.gca().add_patch(rectangle)

        # Segmentation mask
        plt.imshow(
            mask,
            alpha=0.35
        )

        # Label
        plt.text(
            x1,
            y1,
            f"{class_name} {confidence:.2f}",
            fontsize=10,
            backgroundcolor="white"
        )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        output_path,
        bbox_inches="tight"
    )

    plt.close()