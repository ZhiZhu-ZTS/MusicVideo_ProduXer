# MusicVideo_ProduXer
An MV automatic generation project that integrates multiple models, capable of providing end-to-end MV generation starting from lyrics or lyric descriptions, and supporting mid-process monitoring and optimisation through multiple iterations.

# 从suno AI开始
因为suno AI并没有开源或者开放API调用，故我们很遗憾的宣布，suno AI生成音乐部分，我们无法写成一个稳定的程序    
诸位需要移步 https://suno.com/create 进行歌曲创作，所幸suno AI是有免费额度的    
或者您可以选取我们example/input_music中的文件进行试运行    
suno AI生成的结果，请重命名为input.mp3或input.wav，保存在input中    
至于歌词，请调用LLM模型，它会做好的，注意制作歌词并提交给suno AI之前，请确保歌词中带有（前奏）（间奏）（尾奏）的标记，这些标记可以通过AI生成    

# 运行主程序
创建conda或者venv环境，注意python=3.10    
在环境中安装requirements.txt    
至于ffmpeg，请安装ffmpeg并添加至环境变量，注意不只是pip install ffmpeg    

在主程序中，请您键入您的歌词，注意，您键入的歌词中也需要带有（前奏）（间奏）（尾奏）的标记    
等待程序抛出“请确认json”后，再在temp文件夹中，确认json是否符合您的要求，如果不符合，请给主程序指出，如“场景要保持一致”   

抽卡图片仅会在有人的段落中出现，在temp文件夹中，确认图片是否符合要求，如果不符合，程序会抛出prompt，请你修改prompt之后再输入，当你确认后，图片会被从temp文件夹移入temp/picture文件夹并编号    

抽卡视频时，和图片的操作一致    

视频生成后，程序会读取音频并进行切割，然后使用temp/video中的视频进行结合    

最后程序使用ffmpeg，通过temp中的.srt文件为MV提供字幕
