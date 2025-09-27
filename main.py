from shots_manager import ShotsManager

if __name__ == "__main__":
    manager = ShotsManager("shoted.json", output_dir="output")

    # 列出所有 shots
    manager.list_shots()

    description_dir = manager.generate_reference()
    for shot in manager.shots:
        shot.edit_image(base_img_path=description_dir)
        shot.generate_video(use_image=True)