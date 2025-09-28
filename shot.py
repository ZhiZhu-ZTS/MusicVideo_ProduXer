import os
import datetime
from pathlib import Path
from SeedreamImageGenerator import SeedreamImageGenerator
from HailuoVideoGenerator import HailuoVideoGenerator


class Shot:
    def __init__(self, hailuo_client:HailuoVideoGenerator, seedream_client:SeedreamImageGenerator, shot_config: dict, output_dir: str = "outputs"):
        self.id = shot_config["id"]
        self.lyric = shot_config.get("lyric", "")
        self.stable = shot_config.get("stable", "")
        self.dynamic = shot_config.get("dynamic", "")
        self.duration = shot_config.get("duration", 4)
        self.sing = shot_config.get("sing", False)

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # API 客户端
        self.seedream = seedream_client
        self.hailuo = hailuo_client

        # 中间结果
        self.image_path = None
        self.video_path = None

    # --- 抽卡：生成一张候选图像 ---
    def generate_image(self, prompt: str = None, filename: str = None):
        prompt = prompt or self.stable
        # 以时间作为唯一标识
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename or f"shot_{self.id}_image_{timestamp}.png"
        save_path = str(self.output_dir / filename)

        url = self.seedream.generate_image(prompt=prompt, size="2K")
        self.seedream.save_image_from_url(url, save_path)
        self.image_path = save_path
        print(f"✅ Shot {self.id}: 图像已保存 {save_path}")
        return save_path
    
    def edit_image(self, base_img_path, prompt: str = None, filename: str = None):
        assert base_img_path
        prompt = prompt or self.stable
        # 以时间作为唯一标识
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename or f"shot_{self.id}_image_{timestamp}.png"
        save_path = str(self.output_dir / filename)

        url = self.seedream.edit_image(base_image_path=base_img_path, prompt=prompt)
        self.seedream.save_image_from_url(url, save_path)
        self.image_path = save_path
        print(f"✅ Shot {self.id}: 图像已保存 {save_path}")
        return save_path

    # --- 调用 hailuo 视频生成 ---
    def generate_video(self, prompt: str = None, filename: str = None, use_image: bool = True):
        prompt = prompt or f"{self.stable}, {self.dynamic}"
        # 以时间作为唯一标识
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename or f"shot_{self.id}_video_{timestamp}.mp4"
        save_path = str(self.output_dir / filename)

        if use_image and self.image_path:
            task_id = self.hailuo.invoke_image_to_video(prompt, self.image_path)
        else:
            task_id = self.hailuo.invoke_text_to_video(prompt)

        file_id = self.hailuo.query_task_status(task_id)
        print("shot的file_id:", file_id)
        print("shot的save_path:", save_path)
        self.hailuo.fetch_video(file_id, save_path)  # 🔥 直接传完整路径
        self.video_path = save_path
        return save_path

