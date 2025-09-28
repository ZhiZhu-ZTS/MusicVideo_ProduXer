from shots_manager import ShotsManager

if __name__ == "__main__":
    manager = ShotsManager("shots.json", output_dir="output1")

    # 列出所有 shots
    manager.list_shots()

    description_dir = manager.generate_reference()
    for shot in manager.shots:
        shot.edit_image(base_img_path=description_dir)
        a = input("continue?[y/n]")
        if (a == 'n'):
            break
        shot.generate_video(use_image=True)
        a = input("continue?[y/n]")
        if (a == 'n'):
            break