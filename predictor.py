import torch

from PIL import Image
from torchvision.transforms import functional as F
from torchvision.models.detection import (
    maskrcnn_resnet50_fpn,
    MaskRCNN_ResNet50_FPN_Weights
)


COCO_CLASSES = [
    "__background__",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush"
]


class MaskRCNNPredictor:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        weights_path = "/app/model/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth"

        self.model = maskrcnn_resnet50_fpn(
            weights=None
        )

        self.model.load_state_dict(
            torch.load(
                weights_path,
                map_location=self.device,
                weights_only=True
            )
        )

        self.model.to(self.device)

        self.model.eval()

    def predict(self, image):

        image_tensor = F.to_tensor(image).to(self.device)

        with torch.no_grad():

            predictions = self.model(
                [image_tensor]
            )

        prediction = predictions[0]

        results = []

        for box, label, score, mask in zip(
            prediction["boxes"],
            prediction["labels"],
            prediction["scores"],
            prediction["masks"]
        ):

            score_value = score.item()

            if score_value < 0.5:
                continue

            class_id = label.item()

            class_name = COCO_CLASSES[class_id]

            box_values = box.cpu().tolist()

            mask_values = (
                mask[0].cpu().numpy() > 0.5
            )

            results.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": score_value,
                "box": box_values,
                "mask": mask_values
            })

        return results