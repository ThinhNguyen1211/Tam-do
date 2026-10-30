"""Question bank: 104 items, 26 per dichotomy, half keyed to each pole.

`direction` says which pole agreement points to:
  +1 -> first letter of the dichotomy (E, S, T, J)
  -1 -> second letter            (I, N, F, P)

Balancing the keying within each dichotomy cancels out acquiescence bias
(the tendency to agree with statements regardless of content).

IDs are part of the public API (clients submit them back), so never renumber
or reuse an ID; retire a question by removing it and add new ones as q105+.
"""

from dataclasses import dataclass
from typing import Literal

Dichotomy = Literal["EI", "SN", "TF", "JP"]
DICHOTOMIES: tuple[Dichotomy, ...] = ("EI", "SN", "TF", "JP")


@dataclass(frozen=True, slots=True)
class Question:
    id: str
    dichotomy: Dichotomy
    direction: Literal[1, -1]
    text: str
    text_en: str


QUESTIONS: tuple[Question, ...] = (
    # --- E / I: where attention and energy flow ---------------------------------
    Question("q1", "EI", 1, "Sau một ngày dài, tôi thấy được nạp lại năng lượng khi gặp gỡ và trò chuyện với mọi người.", "After a long day, I recharge by spending time with other people."),
    Question("q2", "EI", 1, "Tôi thường làm rõ suy nghĩ của mình bằng cách nói chúng thành lời với người khác.", "I often clarify my thoughts by talking them through with others."),
    Question("q3", "EI", 1, "Khi ở trong một nhóm mới, tôi thường là người chủ động bắt chuyện trước.", "In a new group, I'm usually the one who starts conversations."),
    Question("q4", "EI", 1, "Tôi làm việc hứng khởi hơn trong môi trường có nhiều trao đổi và tương tác.", "I feel more energized working in an environment with lots of interaction."),
    Question("q5", "EI", 1, "Khi có chuyện vui, tôi muốn chia sẻ ngay với nhiều người.", "When something good happens, I want to share it with people right away."),
    Question("q6", "EI", 1, "Tôi thấy thoải mái khi là người dẫn dắt một cuộc thảo luận.", "I'm comfortable being the one who leads a discussion."),
    Question("q7", "EI", 1, "Tôi thích có nhiều mối quan hệ quen biết ở nhiều lĩnh vực khác nhau.", "I enjoy having a wide circle of acquaintances across different areas."),
    Question("q8", "EI", 1, "Khi gặp vấn đề, phản xạ đầu tiên của tôi là tìm ai đó để bàn bạc.", "When facing a problem, my first instinct is to find someone to talk it over with."),
    Question("q9", "EI", 1, "Những khoảng thời gian dài ở một mình khiến tôi thấy bồn chồn.", "Long stretches of time alone make me restless."),
    Question("q10", "EI", 1, "Sự chú ý của tôi tự nhiên hướng ra những gì đang diễn ra xung quanh.", "My attention naturally goes to what's happening around me."),
    Question("q11", "EI", 1, "Tôi thường bắt tay vào làm trước rồi mới suy ngẫm lại sau.", "I tend to jump in first and reflect afterward."),
    Question("q12", "EI", 1, "Tôi tiếp thu tốt hơn qua thảo luận nhóm so với tự đọc một mình.", "I learn better through group discussion than through reading alone."),
    Question("q13", "EI", 1, "Một cuối tuần lý tưởng với tôi là có nhiều hoạt động cùng người khác.", "My ideal weekend is full of activities with other people."),
    Question("q14", "EI", -1, "Sau khi giao tiếp nhiều, tôi cần thời gian yên tĩnh một mình để lấy lại năng lượng.", "After a lot of socializing, I need quiet time alone to recharge."),
    Question("q15", "EI", -1, "Tôi thường suy nghĩ thấu đáo trong đầu trước khi nói ra ý kiến.", "I usually think things through internally before voicing an opinion."),
    Question("q16", "EI", -1, "Tôi thích những cuộc trò chuyện sâu với một hai người hơn là trò chuyện trong nhóm đông.", "I prefer deep conversations with one or two people over chatting in a large group."),
    Question("q17", "EI", -1, "Tôi làm việc hiệu quả nhất khi có không gian riêng và ít bị gián đoạn.", "I do my best work in my own space with few interruptions."),
    Question("q18", "EI", -1, "Tôi thường giữ những suy nghĩ quan trọng cho riêng mình một thời gian trước khi chia sẻ.", "I often keep important thoughts to myself for a while before sharing them."),
    Question("q19", "EI", -1, "Những sự kiện đông người khiến tôi nhanh mệt, kể cả khi tôi thấy vui.", "Crowded events tire me quickly, even when I'm enjoying them."),
    Question("q20", "EI", -1, "Tôi thích quan sát một tình huống mới một lúc trước khi tham gia.", "I like to observe a new situation for a while before joining in."),
    Question("q21", "EI", -1, "Thế giới nội tâm của tôi — suy nghĩ, ý tưởng, ký ức — thường chiếm phần lớn sự chú ý của tôi.", "My inner world of thoughts, ideas and memories usually holds most of my attention."),
    Question("q22", "EI", -1, "Tôi diễn đạt bản thân qua chữ viết dễ hơn là nói ngay tại chỗ.", "I express myself more easily in writing than by speaking on the spot."),
    Question("q23", "EI", -1, "Tôi trân trọng một vài mối quan hệ thân thiết hơn là một mạng lưới quen biết rộng.", "I value a few close relationships more than a broad network."),
    Question("q24", "EI", -1, "Khi có cuộc gọi bất ngờ, tôi thường muốn để lỡ rồi nhắn lại sau.", "When I get an unexpected call, I'd often rather let it ring and reply later."),
    Question("q25", "EI", -1, "Tôi thấy khá dễ chịu khi dành trọn một ngày ở một mình.", "I'm quite content spending a whole day by myself."),
    Question("q26", "EI", -1, "Trong các cuộc họp, tôi thường lắng nghe nhiều hơn là nói.", "In meetings, I usually listen more than I speak."),
    # --- S / N: how information is taken in ---------------------------------------
    Question("q27", "SN", 1, "Tôi tin vào những gì đã được kiểm chứng qua kinh nghiệm hơn là những giả thuyết chưa thử.", "I trust what experience has proven more than untested theories."),
    Question("q28", "SN", 1, "Khi học điều mới, tôi muốn có hướng dẫn cụ thể theo từng bước.", "When learning something new, I want concrete step-by-step instructions."),
    Question("q29", "SN", 1, "Tôi thường để ý những chi tiết nhỏ mà người khác bỏ qua.", "I notice small details that others overlook."),
    Question("q30", "SN", 1, "Tôi thích tập trung vào những gì đang diễn ra hơn là suy đoán về tương lai.", "I'd rather focus on what's happening now than speculate about the future."),
    Question("q31", "SN", 1, "Khi kể lại một sự việc, tôi thường thuật lại chính xác những gì đã xảy ra.", "When recounting an event, I describe exactly what happened."),
    Question("q32", "SN", 1, "Tôi đánh giá cao những giải pháp thực tế, có thể áp dụng ngay.", "I value practical solutions that can be applied right away."),
    Question("q33", "SN", 1, "Tôi thích cải tiến một phương pháp đã có hơn là nghĩ ra một cách làm hoàn toàn mới.", "I'd rather refine an existing method than invent an entirely new one."),
    Question("q34", "SN", 1, "Số liệu và sự kiện cụ thể thuyết phục tôi hơn những ý tưởng trừu tượng.", "Concrete facts and figures convince me more than abstract ideas."),
    Question("q35", "SN", 1, "Tôi dễ ghi nhớ những thông tin cụ thể như ngày tháng, con số, địa điểm.", "I easily remember specifics like dates, numbers and places."),
    Question("q36", "SN", 1, "Tôi thích những công việc có kết quả hữu hình, nhìn thấy được.", "I enjoy work that produces tangible, visible results."),
    Question("q37", "SN", 1, "Tôi hiểu một khái niệm tốt nhất qua ví dụ thực tế.", "I understand a concept best through real-world examples."),
    Question("q38", "SN", 1, "Trước khi thử điều gì mới, tôi muốn biết nó đã từng thành công ở đâu đó.", "Before trying something new, I want to know it has worked somewhere before."),
    Question("q39", "SN", 1, "Tôi chú ý nhiều đến cảm nhận giác quan và môi trường — âm thanh, mùi vị, chất liệu.", "I'm very attentive to sensory experience — sounds, tastes, textures."),
    Question("q40", "SN", -1, "Tôi bị cuốn hút bởi những khả năng và ý nghĩa ẩn sau sự việc.", "I'm drawn to the possibilities and meanings behind things."),
    Question("q41", "SN", -1, "Tôi hay tự hỏi \"nếu như…\" và hình dung ra nhiều kịch bản khác nhau.", "I often ask \"what if…\" and imagine different scenarios."),
    Question("q42", "SN", -1, "Tôi thích nắm bức tranh tổng thể trước rồi mới đi vào chi tiết.", "I like to grasp the big picture before getting into details."),
    Question("q43", "SN", -1, "Tôi dễ nhận ra mối liên hệ giữa những ý tưởng tưởng chừng không liên quan.", "I easily see links between ideas that seem unrelated."),
    Question("q44", "SN", -1, "Tôi thấy hứng thú với lý thuyết và khái niệm, ngay cả khi chưa có ứng dụng ngay.", "I enjoy theories and concepts even without an immediate application."),
    Question("q45", "SN", -1, "Khi đọc, tôi chú ý đến ẩn ý và biểu tượng nhiều hơn nội dung bề mặt.", "When reading, I pay more attention to subtext and symbolism than to surface content."),
    Question("q46", "SN", -1, "Tôi thường có linh cảm về điều sắp xảy ra mà khó giải thích được lý do.", "I often have hunches about what's coming that I can't fully explain."),
    Question("q47", "SN", -1, "Làm theo một quy trình lặp đi lặp lại khiến tôi nhanh chán.", "Following a repetitive routine bores me quickly."),
    Question("q48", "SN", -1, "Tôi hay nghĩ về tương lai và những gì có thể trở thành.", "I often think about the future and what could be."),
    Question("q49", "SN", -1, "Khi kể chuyện, tôi thường truyền tải ý nghĩa hơn là liệt kê chi tiết.", "When telling a story, I convey its meaning more than its details."),
    Question("q50", "SN", -1, "Tôi thích tìm ra cách làm mới, kể cả khi cách cũ vẫn hiệu quả.", "I like finding new ways of doing things, even when the old way still works."),
    Question("q51", "SN", -1, "Tôi hay dùng ẩn dụ và hình ảnh so sánh để giải thích ý tưởng.", "I often use metaphors and analogies to explain ideas."),
    Question("q52", "SN", -1, "Đôi khi tôi bỏ lỡ chi tiết thực tế vì đang mải suy nghĩ về ý tưởng.", "I sometimes miss practical details because I'm absorbed in ideas."),
    # --- T / F: how decisions are made --------------------------------------------
    Question("q53", "TF", 1, "Khi ra quyết định, tôi ưu tiên phân tích logic khách quan.", "When making decisions, I prioritize objective logical analysis."),
    Question("q54", "TF", 1, "Tôi cho rằng góp ý thẳng thắn, rõ ràng là một cách tôn trọng người khác.", "I believe direct, clear feedback is a way of respecting people."),
    Question("q55", "TF", 1, "Tôi nhanh chóng nhận ra điểm thiếu nhất quán trong một lập luận.", "I quickly spot inconsistencies in an argument."),
    Question("q56", "TF", 1, "Công bằng, với tôi, là áp dụng cùng một tiêu chuẩn cho tất cả mọi người.", "To me, fairness means applying the same standard to everyone."),
    Question("q57", "TF", 1, "Tôi có thể tạm gác cảm xúc cá nhân sang một bên khi đánh giá một vấn đề.", "I can set my personal feelings aside when evaluating an issue."),
    Question("q58", "TF", 1, "Bằng chứng và lý lẽ thuyết phục tôi hơn một câu chuyện cảm động.", "Evidence and reasoning persuade me more than a moving story."),
    Question("q59", "TF", 1, "Khi bạn bè kể về một rắc rối, phản xạ của tôi là giúp họ tìm cách giải quyết.", "When a friend shares a problem, my instinct is to help them solve it."),
    Question("q60", "TF", 1, "Tôi thích tranh luận như một cách để kiểm tra độ vững của ý tưởng.", "I enjoy debate as a way to test how solid ideas are."),
    Question("q61", "TF", 1, "Hiệu quả và năng lực là tiêu chí chính khi tôi đánh giá một công việc.", "Effectiveness and competence are my main criteria for judging work."),
    Question("q62", "TF", 1, "Tôi thà nói ra một sự thật khó nghe còn hơn để người khác hiểu sai.", "I'd rather state an uncomfortable truth than let someone be misled."),
    Question("q63", "TF", 1, "Tôi tự hỏi \"điều này có hợp lý không?\" trước khi hỏi \"mọi người sẽ cảm thấy thế nào?\".", "I ask \"does this make sense?\" before \"how will people feel?\""),
    Question("q64", "TF", 1, "Tôi chấp nhận đưa ra quyết định không được lòng số đông nếu nó đúng về mặt logic.", "I'm willing to make an unpopular decision if it's logically sound."),
    Question("q65", "TF", 1, "Khi phân tích vấn đề, tôi tìm nguyên nhân gốc rễ theo chuỗi nhân quả.", "When analyzing a problem, I trace the chain of cause and effect to its root."),
    Question("q66", "TF", -1, "Khi ra quyết định, tôi cân nhắc nhiều đến ảnh hưởng của nó lên con người.", "When making decisions, I weigh heavily how they will affect people."),
    Question("q67", "TF", -1, "Tôi cố gắng góp ý một cách tế nhị để giữ gìn cảm xúc của người khác.", "I try to give feedback tactfully to protect others' feelings."),
    Question("q68", "TF", -1, "Sự hòa hợp trong tập thể rất quan trọng đối với tôi.", "Harmony within a group matters a great deal to me."),
    Question("q69", "TF", -1, "Công bằng, với tôi, là xem xét hoàn cảnh riêng của từng người.", "To me, fairness means taking each person's circumstances into account."),
    Question("q70", "TF", -1, "Tôi dễ cảm nhận được tâm trạng của người khác ngay cả khi họ không nói ra.", "I can sense other people's moods even when they don't say anything."),
    Question("q71", "TF", -1, "Những giá trị cá nhân là kim chỉ nam cho các lựa chọn quan trọng của tôi.", "My personal values guide my important choices."),
    Question("q72", "TF", -1, "Khi bạn bè kể về một rắc rối, trước hết tôi muốn lắng nghe và thấu hiểu họ.", "When a friend shares a problem, I first want to listen and understand them."),
    Question("q73", "TF", -1, "Tôi thấy khó xử khi phải phê bình ai đó, kể cả khi lời phê bình là xác đáng.", "I feel uneasy criticizing someone, even when the criticism is fair."),
    Question("q74", "TF", -1, "Một câu chuyện thật về con người có thể thay đổi quan điểm của tôi nhiều hơn số liệu thống kê.", "A true human story can change my view more than statistics can."),
    Question("q75", "TF", -1, "Tôi thường đặt mình vào vị trí người khác trước khi đánh giá hành động của họ.", "I put myself in someone's shoes before judging their actions."),
    Question("q76", "TF", -1, "Công việc trở nên ý nghĩa với tôi khi nó giúp ích được cho người khác.", "Work feels meaningful to me when it helps other people."),
    Question("q77", "TF", -1, "Tôi sẵn sàng linh động với quy định nếu điều đó giúp được một người đang khó khăn.", "I'm willing to be flexible with rules to help someone who is struggling."),
    Question("q78", "TF", -1, "Sự ghi nhận chân thành có tác động lớn đến động lực của tôi.", "Sincere appreciation has a big effect on my motivation."),
    # --- J / P: how one relates to the outer world ------------------------------
    Question("q79", "JP", 1, "Tôi thích lên kế hoạch trước hơn là tùy cơ ứng biến.", "I prefer planning ahead to improvising."),
    Question("q80", "JP", 1, "Tôi cảm thấy nhẹ nhõm khi một quyết định đã được chốt.", "I feel relieved once a decision is settled."),
    Question("q81", "JP", 1, "Tôi thường hoàn thành công việc sớm, trước hạn chót khá lâu.", "I usually finish tasks well before the deadline."),
    Question("q82", "JP", 1, "Danh sách việc cần làm giúp tôi cảm thấy chủ động trong cuộc sống.", "To-do lists help me feel on top of my life."),
    Question("q83", "JP", 1, "Tôi thích làm xong một việc rồi mới bắt đầu việc khác.", "I like to finish one thing before starting the next."),
    Question("q84", "JP", 1, "Những thay đổi kế hoạch vào phút chót khiến tôi khó chịu.", "Last-minute changes of plan bother me."),
    Question("q85", "JP", 1, "Tôi tập trung tốt hơn khi mọi thứ xung quanh được sắp xếp có trật tự.", "I focus better when things around me are in order."),
    Question("q86", "JP", 1, "Tôi thích biết trước một ngày của mình sẽ diễn ra như thế nào.", "I like knowing in advance how my day will go."),
    Question("q87", "JP", 1, "Khi đi du lịch, tôi muốn có lịch trình cụ thể.", "When traveling, I want a concrete itinerary."),
    Question("q88", "JP", 1, "Khi đã có đủ thông tin cần thiết, tôi đưa ra kết luận khá nhanh.", "Once I have enough information, I reach conclusions fairly quickly."),
    Question("q89", "JP", 1, "Tôi đặt mục tiêu rõ ràng và theo dõi tiến độ của mình.", "I set clear goals and track my progress."),
    Question("q90", "JP", 1, "Tôi thấy thoải mái nhất khi nghỉ ngơi sau khi đã xong việc.", "I relax best once the work is done."),
    Question("q91", "JP", 1, "Tôi thích làm việc với quy trình và hệ thống rõ ràng.", "I like working with clear processes and systems."),
    Question("q92", "JP", -1, "Tôi thích để ngỏ các lựa chọn càng lâu càng tốt.", "I like to keep my options open as long as possible."),
    Question("q93", "JP", -1, "Tôi thường làm việc hiệu quả nhất khi hạn chót đã đến gần.", "I often work best as a deadline approaches."),
    Question("q94", "JP", -1, "Tôi thấy thoải mái khi kế hoạch thay đổi bất ngờ.", "I'm comfortable when plans change unexpectedly."),
    Question("q95", "JP", -1, "Tôi thích khám phá nhiều hướng đi trước khi cam kết với một hướng.", "I like exploring several paths before committing to one."),
    Question("q96", "JP", -1, "Tôi thường làm nhiều việc cùng lúc và chuyển qua lại giữa chúng một cách tự nhiên.", "I often juggle several tasks and move between them freely."),
    Question("q97", "JP", -1, "Một lịch trình quá kín khiến tôi thấy gò bó.", "A tightly packed schedule feels confining to me."),
    Question("q98", "JP", -1, "Khi đi du lịch, tôi thích để mỗi ngày tự diễn ra một cách tự nhiên.", "When traveling, I like to let each day unfold on its own."),
    Question("q99", "JP", -1, "Tôi muốn thu thập thêm thông tin hơn là vội vàng đưa ra quyết định.", "I'd rather gather more information than rush to a decision."),
    Question("q100", "JP", -1, "Tôi thấy những quy định cứng nhắc thường cản trở sự sáng tạo.", "I find rigid rules often get in the way of creativity."),
    Question("q101", "JP", -1, "Tôi thích bắt tay vào làm rồi điều chỉnh dần hơn là lập kế hoạch chi tiết từ đầu.", "I prefer to start and adjust along the way rather than plan everything up front."),
    Question("q102", "JP", -1, "Tôi dễ dàng thích nghi với những tình huống không lường trước.", "I adapt easily to situations I didn't anticipate."),
    Question("q103", "JP", -1, "Tôi tận hưởng quá trình làm việc nhiều hơn khoảnh khắc hoàn thành.", "I enjoy the process of working more than the moment of finishing."),
    Question("q104", "JP", -1, "Tôi luôn sẵn sàng đổi ý nếu có thông tin mới xuất hiện.", "I'm always open to changing my mind when new information comes up."),
)

QUESTIONS_BY_ID: dict[str, Question] = {q.id: q for q in QUESTIONS}

QUESTIONS_BY_DICHOTOMY: dict[Dichotomy, tuple[Question, ...]] = {
    d: tuple(q for q in QUESTIONS if q.dichotomy == d) for d in DICHOTOMIES
}
