from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx import resize
from moviepy.video.tools.segmenting import findObjects


# 导入字幕
generator = lambda txt: TextClip(txt, font='SimHei', fontsize=24, color='black')
sub = SubtitlesClip("welcome.srt", generator)
txt_clip = TextClip("good！", fontsize=70, color='white')
txt_clip = txt_clip.set_pos('center').set_duration(10)
# 片头
start_clip = VideoFileClip("start_clip.mp4").subclip(0, 3.0).rotate(90).resize((1500, 750))
# 合成字幕
# start_clip = CompositeVideoClip([start_clip, sub])
# start_clip = CompositeVideoClip([start_clip, txt_clip])
# 片尾
end_clip = ImageClip("end.jpg")
end_clip = end_clip.set_duration(2).resize((1500, 750))

# 内容
main_clip = VideoFileClip("wzj-20190917.wmv", audio=False).without_audio().subclip(0, 10.0).on_color(color=(255, 255, 255)).resize((1050, 750)).crossfadein(0.5).crossfadeout(0.5)
left_clip1 = VideoFileClip("left_clip.mp4", audio=False).without_audio().subclip(0, 10.0).rotate(90).on_color(color=(255, 255, 255))


# 另一种实现，通过画好的线框来安置视频
# Load the image specifying the regions.
im = ImageClip("BACK.png").resize((1500, 750))
# Loacate the regions, return a list of ImageClips
regions = findObjects(im)
clips = [left_clip1, main_clip]
comp_clips = [c.resize(r.size).set_mask(r.mask).set_position(r.screenpos) for c, r in zip(clips, regions)]

mid_clip = CompositeVideoClip(comp_clips, im.size)

# 剪辑合成
final_clip = concatenate_videoclips([start_clip, mid_clip, end_clip])
# 输出视频
final_clip.write_videofile("my_stack.mp4", fps=10)
