from shots_manager import ShotsManager
from shot import Shot
import concurrent.futures
import os

def process_shot(shot:Shot, description_dir):
    character_in_scene = shot.character_in_scene
    if character_in_scene:
        shot.edit_image(base_img_path=description_dir)
        shot.generate_video(use_image=True)
    else:
        shot.generate_video(use_image=False)
    
    return f"Completed processing shot {shot.id}"

if __name__ == "__main__":
    manager = ShotsManager("shots.json", output_dir="output4")

    # 列出所有 shots
    manager.list_shots()

    description_dir = manager.generate_reference()
    
    # 使用线程池并行处理
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交所有shot的处理任务
        futures = [executor.submit(process_shot, shot, description_dir) for shot in manager.shots]
        
        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Error processing shot: {e}")