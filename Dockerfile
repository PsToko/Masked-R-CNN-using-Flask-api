FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/model

RUN python -c "import urllib.request; urllib.request.urlretrieve('https://download.pytorch.org/models/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth', '/app/model/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth')"

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]