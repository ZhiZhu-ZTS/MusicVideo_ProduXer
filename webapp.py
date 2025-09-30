import gradio as gr
from shots_manager import ShotsManager
from shot import Shot
from typing import List, Dict, Any
import os

class MVGeneratorUI:
    def __init__(self, shots_json_path: str = "shots.json"):
        self.manager = ShotsManager(shots_json_path)
        self.current_shots_data = []
    
    def initialize_manager(self):
        """初始化管理器"""
        try:
            self.manager = ShotsManager("shots.json")
            return "✅ 管理器初始化成功"
        except Exception as e:
            return f"❌ 初始化失败: {str(e)}"
    
    def list_shots(self) -> List[List[Any]]:
        """获取分镜列表数据"""
        self.current_shots_data = []
        for shot in self.manager.shots:
            self.current_shots_data.append([
                shot.id,
                shot.lyric,
                shot.stable,
                shot.dynamic,
                shot.duration,
                shot.sing
            ])
        return self.current_shots_data
    
    def generate_reference(self):
        """生成角色参考图"""
        try:
            path = self.manager.generate_reference()
            return path, "✅ 角色参考图生成成功"
        except Exception as e:
            return None, f"❌ 生成失败: {str(e)}"
    
    def create_shot_management_section(self) -> gr.Blocks:
        """创建分镜管理部分（角色参考 + 分镜列表）"""
        with gr.Blocks() as section:
            gr.Markdown("## 🎭 角色参考与分镜管理")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 角色参考图")
                    ref_btn = gr.Button("生成角色参考图", variant="primary")
                    ref_status = gr.Textbox(label="状态", interactive=False)
                    ref_img = gr.Image(label="角色参考图", type="filepath", height=500)
                
                with gr.Column(scale=2):
                    gr.Markdown("### 分镜列表")
                    with gr.Row():
                        load_btn = gr.Button("刷新分镜列表", variant="secondary")
                        init_btn = gr.Button("重新初始化", variant="secondary")
                    
                    init_status = gr.Textbox(label="初始化状态", interactive=False)
                    shots_table = gr.Dataframe(
                        headers=["ID", "歌词", "静态Prompt", "动态Prompt", "时长", "是否唱歌"],
                        datatype=["number", "str", "str", "str", "number", "bool"],
                        interactive=False,
                        max_height=500
                    )
            
            # 事件绑定
            ref_btn.click(
                fn=self.generate_reference,
                outputs=[ref_img, ref_status]
            )
            
            load_btn.click(
                fn=self.list_shots,
                outputs=shots_table
            )
            
            init_btn.click(
                fn=self.initialize_manager,
                outputs=init_status
            ).then(
                fn=self.list_shots,
                outputs=shots_table
            )
        
        return section
    
    def create_shot_detail_section(self, shot_index: int) -> gr.Blocks:
        """为单个shot创建详细操作页面"""
        shot = self.manager.shots[shot_index]
        shot_id = shot.id
        with gr.Blocks() as section:
            gr.Markdown(f"## 🎬 分镜 {shot_id} 详情")
            
            with gr.Row():
                gr.Markdown(f"**歌词:** {shot.lyric}")
                gr.Markdown(f"**时长:** {shot.duration}秒")
                gr.Markdown(f"**唱歌:** {'是' if shot.sing else '否'}")
            
            with gr.Tabs():
                # Tab 1: 图像生成
                with gr.TabItem("🖼️ 图像生成"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 修改第一帧图像")
                            edit_img_input = gr.Image(
                                label="上传参考图进行修改",
                                type="filepath",
                                height=200,
                                value=self.manager.reference_pic_dir
                            )
                            edit_prompt = gr.Textbox(
                                label="修改Prompt (可选)",
                                value=shot.stable,
                                lines=2
                            )
                            edit_img_btn = gr.Button("修改图像", variant="secondary")
                            edit_status = gr.Textbox(label="状态", interactive=False)
                    
                    img_output = gr.Image(
                        label="图像预览",
                        type="filepath",
                        height=400
                    )
                    
                    # 图像修改事件
                    
                    edit_img_btn.click(
                        fn=lambda img, prompt: self._edit_first_frame(shot_index, img, prompt),
                        inputs=[edit_img_input, edit_prompt],
                        outputs=[img_output, edit_status]
                    )
                
                # Tab 2: 视频生成
                with gr.TabItem("🎥 视频生成"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 生成视频")
                            video_prompt = gr.Textbox(
                                label="视频Prompt (可选)",
                                value=shot.dynamic,
                                lines=2
                            )
                            video_duration = gr.Number(
                                label="视频时长(秒)",
                                value=shot.duration
                            )
                            video_btn = gr.Button("生成视频", variant="primary")
                            video_status = gr.Textbox(label="状态", interactive=False)
                        
                        with gr.Column():
                            gr.Markdown("### Prompt说明")
                            gr.Markdown(f"**静态Prompt:** {shot.stable}")
                            gr.Markdown(f"**动态Prompt:** {shot.dynamic}")
                    
                    video_output = gr.Video(
                        label="视频预览",
                        height=400
                    )
                    
                    video_btn.click(
                        fn=lambda prompt, duration: self._generate_video(shot_id, prompt, duration),
                        inputs=[video_prompt, video_duration],
                        outputs=[video_output, video_status]
                    )
        
        return section
    
    def _generate_image(self, shot_index: int, prompt: str = None):
        """生成图像（内部方法）"""
        try:
            shot = self.manager.shots[shot_index]
            shot_id = shot.id
            path = shot.generate_image(prompt=prompt)
            return path, f"✅ 分镜 {shot_id} 图像生成成功"
        except Exception as e:
            return None, f"❌ 图像生成失败: {str(e)}"
    
    def _edit_first_frame(self, shot_index: int, base_img: str=None, prompt: str = None):
        """修改第一帧图像（内部方法）"""
        try:
            shot=self.manager.shots[shot_index]
            shot_id = shot.id
            path = self.manager.generate_first_frame(shot_index=shot_index, reference_dir=base_img, prompt=prompt)
            return path, f"✅ 分镜 {shot_id} 图像修改成功"
        except Exception as e:
            return None, f"❌ 图像修改失败: {str(e)}"
    
    def _generate_video(self, shot_index: int, prompt: str = None, duration: float = None):
        """生成视频（内部方法）"""
        try:
            shot = self.manager.shots[shot_index]
            shot_id = shot.id
            path = shot.generate_video(prompt=prompt, duration=duration)
            return path, f"✅ 分镜 {shot_id} 视频生成成功"
        except Exception as e:
            return None, f"❌ 视频生成失败: {str(e)}"
    
    def create_ui(self) -> gr.Blocks:
        """创建完整的UI界面"""
        with gr.Blocks(theme=gr.themes.Soft(), title="MV分镜生成工具") as demo:
            gr.Markdown("# 🎬 MV 分镜生成管理工具")
            
            # 主管理区域
            management_section = self.create_shot_management_section()
            
            # 为每个shot创建独立Tab
            if hasattr(self.manager, 'shots') and self.manager.shots:
                gr.Markdown("## 📋 分镜详细操作")
                
                with gr.Tabs() as tabs:
                    # 为每个shot创建一个Tab
                    for shot_index, shot in enumerate(self.manager.shots):
                        with gr.Tab(f"分镜 {shot.id}"):
                            self.create_shot_detail_section(shot_index=shot_index)
            
            return demo

# 使用示例
if __name__ == "__main__":
    # 创建UI实例
    ui = MVGeneratorUI("shots.json")
    
    # 生成UI并启动
    demo = ui.create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False
    )