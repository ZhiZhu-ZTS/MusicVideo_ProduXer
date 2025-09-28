from shots_manager import ShotsManager

if __name__ == "__main__":
    manager = ShotsManager("shots.json", output_dir="output1")

    # 列出所有 shots
    shot = manager.get_shot_by_id(23)
    reference = shot.generate_image()
    shot.edit_image(reference)
    shot.generate_video()