"""Narrative content for the 16 types and the 8 Jungian cognitive functions.

Pure data: the engine decides which pieces to show and assembles them.
Growth areas are phrased as directions to grow toward, never as defects,
and usually point at the less-developed functions of the type's stack.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TypeProfile:
    title_vi: str
    title_en: str
    tagline: str
    core_drivers: str
    cognitive_processing: str
    strengths: tuple[str, ...]
    growth_areas: tuple[str, ...]
    interpersonal: str


FUNCTION_NAMES: dict[str, tuple[str, str]] = {
    "Ni": ("Trực giác hướng nội", "Introverted Intuition"),
    "Ne": ("Trực giác hướng ngoại", "Extraverted Intuition"),
    "Si": ("Cảm nhận hướng nội", "Introverted Sensing"),
    "Se": ("Cảm nhận hướng ngoại", "Extraverted Sensing"),
    "Ti": ("Tư duy hướng nội", "Introverted Thinking"),
    "Te": ("Tư duy hướng ngoại", "Extraverted Thinking"),
    "Fi": ("Cảm xúc hướng nội", "Introverted Feeling"),
    "Fe": ("Cảm xúc hướng ngoại", "Extraverted Feeling"),
}

FUNCTION_DESCRIPTIONS: dict[str, str] = {
    "Ni": "Chắt lọc nhiều tín hiệu rời rạc thành một nhận định hội tụ về ý nghĩa và hướng phát triển của sự việc.",
    "Ne": "Nhận ra khả năng, liên tưởng và tiềm năng chưa được khai phá trong con người, ý tưởng và tình huống.",
    "Si": "Đối chiếu hiện tại với kho kinh nghiệm và cảm nhận đã lưu giữ, tạo nên sự ổn định và tính liên tục.",
    "Se": "Tiếp nhận trọn vẹn thực tại qua các giác quan và phản ứng linh hoạt, tức thời với môi trường.",
    "Ti": "Xây dựng một khuôn khổ logic nội tại, đòi hỏi các khái niệm phải chính xác và nhất quán.",
    "Te": "Tổ chức thế giới bên ngoài theo mục tiêu, bằng chứng và hiệu quả có thể đo lường được.",
    "Fi": "Đánh giá sự việc dựa trên hệ giá trị cá nhân sâu sắc và nhu cầu được sống chân thực.",
    "Fe": "Hướng tới sự hài hòa chung, cảm nhận và đáp ứng nhu cầu cảm xúc của những người xung quanh.",
}

# (Vietnamese label, English label, what this position means for the person)
STACK_POSITIONS: tuple[tuple[str, str, str], ...] = (
    ("Chủ đạo", "Dominant", "Chức năng tự nhiên và đáng tin cậy nhất — nơi bạn cảm thấy là chính mình nhất."),
    ("Hỗ trợ", "Auxiliary", "Cân bằng cho chức năng chủ đạo, thường phát triển rõ nét khi bạn trưởng thành."),
    ("Thứ ba", "Tertiary", "Phát triển dần theo thời gian, mang lại sự linh hoạt và niềm vui khi được sử dụng."),
    ("Tiềm ẩn", "Inferior", "Ít quen thuộc nhất; dễ lộ diện khi căng thẳng, nhưng cũng là cánh cửa trưởng thành lớn nhất."),
)

PROFILES: dict[str, TypeProfile] = {
    "INTJ": TypeProfile(
        title_vi="Nhà Chiến Lược",
        title_en="The Strategist",
        tagline="Nhìn xa, nghĩ sâu, và kiên định biến tầm nhìn thành hiện thực.",
        core_drivers=(
            "Động lực sâu xa của bạn là hiểu được cách mọi thứ vận hành ở tầng sâu nhất, rồi dùng sự hiểu biết đó để định hình tương lai. "
            "Bạn nhìn thế giới như một hệ thống có thể cải thiện: mỗi vấn đề đều có một cấu trúc ẩn đang chờ được giải mã. "
            "Sự độc lập trong tư duy không phải là xa cách, mà là cách bạn giữ cho tầm nhìn của mình không bị pha loãng bởi những ý kiến chưa được kiểm chứng. "
            "Bạn tìm thấy ý nghĩa khi một ý tưởng phức tạp cuối cùng trở thành một kế hoạch rõ ràng và khả thi."
        ),
        cognitive_processing=(
            "Trực giác hướng nội giúp bạn chắt lọc vô số dữ kiện thành một vài nhận định cốt lõi về hướng đi của sự việc — thường là trước khi bạn giải thích được vì sao. "
            "Tư duy hướng ngoại sau đó biến những nhận định ấy thành mục tiêu, cột mốc và tiêu chí đo lường. "
            "Bạn xử lý thông tin theo chiều sâu: chất vấn giả định, tìm mô hình, và mạnh dạn loại bỏ những gì không phục vụ mục tiêu."
        ),
        strengths=(
            "Tư duy hệ thống và khả năng hoạch định dài hạn",
            "Nhận ra xu hướng và hệ quả trước người khác",
            "Tiêu chuẩn cao cùng tinh thần tự học bền bỉ",
            "Bình tĩnh và quyết đoán trước vấn đề phức tạp",
        ),
        growth_areas=(
            "Chia sẻ lập luận phía sau tầm nhìn, không chỉ kết luận, để người khác có thể đồng hành",
            "Đón nhận cảm xúc — của mình và của người khác — như một nguồn dữ liệu chính đáng",
            "Quay về với hiện tại và cơ thể khi căng thẳng, thay vì phân tích thêm",
            "Chấp nhận rằng một kế hoạch đủ tốt được thực hiện sớm đôi khi giá trị hơn một kế hoạch hoàn hảo",
        ),
        interpersonal=(
            "Bạn thể hiện sự quan tâm qua hành động: giải quyết vấn đề cho người mình thương, đầu tư thời gian giúp họ phát triển, và trung thực ngay cả khi điều đó khó nói. "
            "Bạn trân trọng những mối quan hệ nơi cả hai được là chính mình mà không cần xã giao. "
            "Sự đồng cảm của bạn thiên về thấu hiểu hơn là biểu lộ — bạn cố nắm bắt điều người kia thực sự cần. "
            "Những ai đủ gần sẽ nhận ra đằng sau vẻ điềm tĩnh là một sự tận tụy rất sâu."
        ),
    ),
    "INTP": TypeProfile(
        title_vi="Nhà Lý Thuyết",
        title_en="The Theorist",
        tagline="Người kiến tạo những mô hình chính xác để hiểu thế giới.",
        core_drivers=(
            "Bạn được thúc đẩy bởi nhu cầu hiểu: không chỉ biết rằng điều gì đó đúng, mà biết vì sao nó đúng và trong điều kiện nào nó sẽ sai. "
            "Thế giới với bạn là một chuỗi câu đố logic đáng để khám phá. "
            "Bạn coi trọng sự chính xác và trung thực trí tuệ, sẵn sàng xét lại cả niềm tin của chính mình khi gặp một lập luận tốt hơn. "
            "Tự do suy nghĩ theo nhịp điệu riêng là điều kiện để bạn tỏa sáng."
        ),
        cognitive_processing=(
            "Tư duy hướng nội xây dựng trong bạn một khuôn khổ logic chặt chẽ, nơi mọi khái niệm cần được định nghĩa rõ ràng và nhất quán. "
            "Trực giác hướng ngoại liên tục mang đến những khả năng, liên tưởng và giả thuyết mới để khuôn khổ ấy kiểm nghiệm. "
            "Bạn xử lý thông tin bằng cách phân rã nó thành các nguyên lý, rồi thử xem chúng có thể ghép lại theo những cách nào."
        ),
        strengths=(
            "Phân tích sắc bén, nhanh chóng phát hiện lỗ hổng lập luận",
            "Tò mò trí tuệ và khả năng tự học sâu",
            "Sáng tạo trong việc kết nối các lĩnh vực khác nhau",
            "Khách quan và cởi mở trước ý kiến trái chiều",
        ),
        growth_areas=(
            "Biến ý tưởng thành sản phẩm cụ thể — hoàn thành quan trọng không kém khám phá",
            "Chia sẻ suy nghĩ sớm hơn, kể cả khi chúng chưa hoàn chỉnh",
            "Nuôi dưỡng kết nối cảm xúc bằng những cử chỉ nhỏ nhưng đều đặn",
            "Xây dựng vài thói quen ổn định để chăm sóc bản thân và giữ nhịp làm việc",
        ),
        interpersonal=(
            "Bạn là người lắng nghe không phán xét, thích những cuộc trò chuyện nơi ý tưởng được trao đổi tự do. "
            "Sự quan tâm của bạn thể hiện qua việc kiên nhẫn giúp người khác suy nghĩ thấu đáo về vấn đề của họ. "
            "Bạn có thể không giỏi những nghi thức xã giao, nhưng sự chân thành của bạn rất đáng tin. "
            "Trong các mối quan hệ, bạn cần có không gian riêng, và đổi lại bạn luôn tôn trọng sự độc lập của người khác."
        ),
    ),
    "ENTJ": TypeProfile(
        title_vi="Nhà Lãnh Đạo Chiến Lược",
        title_en="The Strategic Leader",
        tagline="Biến tầm nhìn thành tổ chức, và tổ chức thành kết quả.",
        core_drivers=(
            "Bạn được thúc đẩy bởi mong muốn tạo ra ảnh hưởng thực sự: xây dựng, tổ chức và dẫn dắt mọi thứ hướng tới những mục tiêu đáng giá. "
            "Bạn nhìn thấy tiềm năng chưa được khai thác trong con người và hệ thống, và cảm thấy có trách nhiệm hiện thực hóa nó. "
            "Sự kém hiệu quả khiến bạn khó chịu không phải vì thiếu kiên nhẫn, mà vì bạn thấy rõ cái giá của những cơ hội bị bỏ lỡ. "
            "Năng lực — của bản thân và của tập thể — là điều bạn trân trọng sâu sắc."
        ),
        cognitive_processing=(
            "Tư duy hướng ngoại là trung tâm: bạn tự nhiên sắp xếp thế giới bên ngoài thành mục tiêu, nguồn lực, trách nhiệm và thước đo. "
            "Trực giác hướng nội hỗ trợ bằng tầm nhìn dài hạn và khả năng dự đoán hệ quả của từng lựa chọn. "
            "Bạn xử lý thông tin nhanh và có định hướng: điều gì quan trọng nhất, ai chịu trách nhiệm, và bước tiếp theo là gì."
        ),
        strengths=(
            "Lãnh đạo quyết đoán trong tình huống phức tạp",
            "Kết hợp tư duy chiến lược với năng lực thực thi",
            "Truyền đạt rõ ràng và thẳng thắn",
            "Phát triển năng lực người khác qua những kỳ vọng cao",
        ),
        growth_areas=(
            "Chậm lại để lắng nghe trọn vẹn trước khi đưa ra giải pháp",
            "Nhận ra những giá trị cá nhân sâu kín đang dẫn dắt mình, và cho phép mình bày tỏ chúng",
            "Ghi nhận nỗ lực của người khác, không chỉ kết quả",
            "Cho phép bản thân nghỉ ngơi mà không cảm thấy có lỗi",
        ),
        interpersonal=(
            "Bạn thể hiện tình cảm bằng sự đầu tư: bạn tin vào tiềm năng của người khác và muốn giúp họ phát huy nó. "
            "Bạn giao tiếp thẳng thắn và mong đợi điều tương tự từ người khác. "
            "Trong các mối quan hệ thân thiết, bạn trung thành và luôn sẵn sàng bảo vệ. "
            "Khi bạn học cách bày tỏ sự dịu dàng ẩn bên trong, những người xung quanh sẽ cảm nhận được bạn quan tâm họ nhiều đến nhường nào."
        ),
    ),
    "ENTP": TypeProfile(
        title_vi="Nhà Cách Tân",
        title_en="The Innovator",
        tagline="Người mở ra những cánh cửa mà người khác chưa nghĩ là tồn tại.",
        core_drivers=(
            "Bạn được thúc đẩy bởi sự hào hứng trước những khả năng mới: mỗi ý tưởng là một cánh cửa dẫn đến nhiều ý tưởng khác. "
            "Bạn nhìn thế giới như một sân chơi trí tuệ, nơi mọi giả định đều có thể được đặt câu hỏi và mọi giới hạn đều có thể được thử thách. "
            "Bạn tôn trọng tư duy độc lập và không chịu được sự trì trệ. "
            "Với bạn, đổi mới không phải là phá bỏ vì muốn phá bỏ, mà là tìm ra một cách tốt hơn cho mọi người."
        ),
        cognitive_processing=(
            "Trực giác hướng ngoại liên tục quét môi trường để tìm mô hình, tiềm năng và những kết nối bất ngờ. "
            "Tư duy hướng nội kiểm định các khả năng ấy bằng logic, chỉ giữ lại những gì thực sự đứng vững. "
            "Bạn xử lý thông tin bằng cách thử nghiệm — đôi khi đứng về phía đối lập chỉ để xem một lập luận chịu được đến đâu."
        ),
        strengths=(
            "Sáng tạo và linh hoạt trong giải quyết vấn đề",
            "Nắm bắt rất nhanh những khái niệm mới",
            "Khả năng truyền cảm hứng và lập luận thuyết phục",
            "Thích nghi tốt trước thay đổi",
        ),
        growth_areas=(
            "Theo đuổi một số ý tưởng đến cùng thay vì chuyển sang ý tưởng mới quá sớm",
            "Để ý người khác cảm nhận cuộc tranh luận ra sao — không phải ai cũng xem đó là một trò chơi",
            "Trân trọng chi tiết, thói quen và kinh nghiệm quá khứ như một nguồn trí tuệ",
            "Chăm sóc những nhu cầu cơ bản của bản thân như giấc ngủ và nhịp sinh hoạt",
        ),
        interpersonal=(
            "Bạn mang năng lượng và sự hài hước đến các mối quan hệ, khiến người khác thấy được khơi gợi trí tuệ. "
            "Bạn quan tâm bằng cách giúp người khác nhìn vấn đề của họ từ một góc độ mới. "
            "Bạn trân trọng những người dám tranh luận với mình một cách cởi mở và tôn trọng. "
            "Khi kết hợp sự sắc sảo với sự ấm áp, bạn trở thành người bạn đồng hành vừa thú vị vừa đáng tin cậy."
        ),
    ),
    "INFJ": TypeProfile(
        title_vi="Người Cố Vấn",
        title_en="The Counselor",
        tagline="Thấu hiểu con người sâu sắc, và lặng lẽ dẫn đường cho điều tốt đẹp.",
        core_drivers=(
            "Bạn được thúc đẩy bởi khát khao tìm ra ý nghĩa và giúp con người phát triển trọn vẹn. "
            "Bạn nhìn thấy những dòng chảy ngầm bên dưới con người và sự kiện, và cảm thấy có trách nhiệm hướng chúng về phía điều tốt. "
            "Sự chân thành và chiều sâu quan trọng với bạn hơn mọi vẻ bề ngoài. "
            "Bạn sống theo một tầm nhìn nội tâm về cách thế giới có thể trở nên nhân văn hơn."
        ),
        cognitive_processing=(
            "Trực giác hướng nội cho bạn khả năng tổng hợp những tín hiệu tinh tế thành sự hiểu biết sâu sắc về con người và tương lai. "
            "Cảm xúc hướng ngoại giúp bạn cảm nhận bầu không khí cảm xúc và điều chỉnh để kết nối mọi người với nhau. "
            "Bạn xử lý thông tin bằng cách tìm ý nghĩa và động cơ ẩn sau hành vi, rồi suy ngẫm xem điều đó sẽ dẫn đến đâu."
        ),
        strengths=(
            "Thấu cảm sâu sắc và trực giác tinh tế về con người",
            "Tầm nhìn dài hạn gắn liền với giá trị",
            "Diễn đạt những ý tưởng phức tạp một cách truyền cảm",
            "Tận tâm và kiên định với điều mình tin tưởng",
        ),
        growth_areas=(
            "Đặt ranh giới lành mạnh để không kiệt sức vì gánh vác cảm xúc của người khác",
            "Kiểm chứng trực giác bằng dữ kiện và đối thoại trước khi đi đến kết luận",
            "Cho phép bản thân — và người khác — được không hoàn hảo",
            "Kết nối với hiện tại qua vận động thể chất để giải tỏa căng thẳng",
        ),
        interpersonal=(
            "Bạn là người lắng nghe sâu, khiến người khác cảm thấy mình thực sự được thấu hiểu. "
            "Bạn thường có ít mối quan hệ nhưng mỗi mối quan hệ đều sâu sắc. "
            "Sự đồng cảm của bạn vừa mang tính cảm xúc vừa mang tính nhận thức — bạn cảm được người kia đang trải qua điều gì và hiểu vì sao. "
            "Hãy nhớ rằng bạn cũng xứng đáng được lắng nghe như cách bạn vẫn lắng nghe người khác."
        ),
    ),
    "INFP": TypeProfile(
        title_vi="Người Lý Tưởng",
        title_en="The Idealist",
        tagline="Trung thành với tiếng nói bên trong, và nhìn thấy điều tốt đẹp trong mỗi người.",
        core_drivers=(
            "Bạn được thúc đẩy bởi mong muốn sống chân thật với giá trị của mình và góp phần làm thế giới tử tế hơn. "
            "Bạn cảm nhận rất rõ điều gì là đúng với bản thân, và tìm kiếm ý nghĩa trong mọi việc mình làm. "
            "Bạn nhìn thấy tiềm năng tốt đẹp trong con người, ngay cả khi chính họ chưa nhận ra. "
            "Với bạn, sự chân thực quan trọng hơn bất kỳ sự công nhận nào từ bên ngoài."
        ),
        cognitive_processing=(
            "Cảm xúc hướng nội là la bàn giá trị: bạn đánh giá mọi thứ dựa trên việc nó có hài hòa với những điều bạn trân quý hay không. "
            "Trực giác hướng ngoại mở ra những khả năng, câu chuyện và cách diễn giải mới. "
            "Bạn xử lý thông tin bằng cách cảm nhận ý nghĩa cá nhân của nó, rồi khám phá những hướng mà nó có thể dẫn tới."
        ),
        strengths=(
            "Chân thành và giàu lòng trắc ẩn",
            "Sáng tạo, giàu trí tưởng tượng",
            "Kiên định với các giá trị đạo đức",
            "Thấu hiểu những góc nhìn khác biệt",
        ),
        growth_areas=(
            "Chuyển lý tưởng thành những bước hành động nhỏ và cụ thể",
            "Đón nhận góp ý như thông tin về công việc, không phải phán xét về con người mình",
            "Chủ động chia sẻ nhu cầu của bản thân thay vì chờ người khác tự nhận ra",
            "Xem những điều chưa hoàn hảo là một phần tự nhiên của mọi quá trình",
        ),
        interpersonal=(
            "Bạn mang đến cho các mối quan hệ sự chấp nhận trọn vẹn và lòng trung thành sâu sắc. "
            "Bạn tôn trọng cá tính riêng của người khác và không cố thay đổi họ. "
            "Sự đồng cảm của bạn thường diễn ra lặng lẽ — bạn cảm nhận rất nhiều nhưng không phải lúc nào cũng nói ra. "
            "Khi bạn dám chia sẻ thế giới nội tâm phong phú của mình, người khác sẽ thấy được một chiều sâu đáng trân trọng."
        ),
    ),
    "ENFJ": TypeProfile(
        title_vi="Người Dẫn Dắt",
        title_en="The Mentor",
        tagline="Kết nối con người và khơi dậy điều tốt đẹp nhất trong họ.",
        core_drivers=(
            "Bạn được thúc đẩy bởi niềm tin rằng con người luôn có thể trưởng thành, và bạn muốn góp phần vào hành trình ấy. "
            "Bạn nhìn thế giới qua lăng kính của các mối quan hệ và tiềm năng con người. "
            "Sự hòa hợp và cảm giác thuộc về một cộng đồng rất quan trọng với bạn. "
            "Bạn tìm thấy ý nghĩa khi giúp một nhóm người cùng hướng về một mục tiêu chung tốt đẹp."
        ),
        cognitive_processing=(
            "Cảm xúc hướng ngoại giúp bạn đọc được nhu cầu và cảm xúc của tập thể, và tự nhiên điều chỉnh để mọi người thấy được kết nối. "
            "Trực giác hướng nội hỗ trợ bằng tầm nhìn về việc mỗi người có thể trở thành ai và cộng đồng có thể đi về đâu. "
            "Bạn xử lý thông tin bằng cách xem nó ảnh hưởng thế nào đến con người, rồi hình dung hướng phát triển phía trước."
        ),
        strengths=(
            "Truyền cảm hứng và gắn kết tập thể",
            "Thấu hiểu nhu cầu của người khác",
            "Giao tiếp ấm áp và thuyết phục",
            "Tận tâm hỗ trợ sự phát triển của người khác",
        ),
        growth_areas=(
            "Chăm sóc nhu cầu của chính mình, không chỉ nhu cầu của người khác",
            "Để người khác tự tìm con đường của họ, kể cả khi bạn thấy một hướng tốt hơn",
            "Phân tích logic một cách độc lập trước những quyết định quan trọng",
            "Nhận ra rằng xung đột lành mạnh có thể làm mối quan hệ bền chặt hơn",
        ),
        interpersonal=(
            "Bạn là chất keo kết nối của nhiều tập thể, luôn để ý xem ai đang bị bỏ lại phía sau. "
            "Sự quan tâm của bạn chủ động và ấm áp — bạn nhớ những điều quan trọng với người khác và hành động vì họ. "
            "Bạn đồng cảm bằng cách cảm nhận và phản hồi lại cảm xúc của người đối diện. "
            "Hãy để người khác cũng có cơ hội được chăm sóc bạn."
        ),
    ),
    "ENFP": TypeProfile(
        title_vi="Người Truyền Cảm Hứng",
        title_en="The Inspirer",
        tagline="Nhìn thấy khả năng ở khắp nơi, và thắp lửa cho những người xung quanh.",
        core_drivers=(
            "Bạn được thúc đẩy bởi sự háo hức trước những khả năng mới và mong muốn sống một cuộc đời chân thực, đầy ý nghĩa. "
            "Bạn nhìn thế giới như một mạng lưới kết nối và tiềm năng đang chờ được khám phá. "
            "Tự do, sáng tạo và sự chân thành là những giá trị cốt lõi của bạn. "
            "Bạn tin rằng mỗi người đều mang trong mình điều gì đó đặc biệt đáng được nhìn thấy."
        ),
        cognitive_processing=(
            "Trực giác hướng ngoại liên tục tạo ra ý tưởng và nhận ra tiềm năng trong con người lẫn tình huống. "
            "Cảm xúc hướng nội giúp bạn chọn ra những khả năng thực sự có ý nghĩa với giá trị của mình. "
            "Bạn xử lý thông tin bằng cách liên tưởng rộng rồi cảm nhận xem điều gì thực sự chạm đến mình."
        ),
        strengths=(
            "Nhiệt huyết và khả năng truyền cảm hứng",
            "Sáng tạo, dồi dào ý tưởng",
            "Thấu hiểu con người và khích lệ tiềm năng của họ",
            "Linh hoạt và cởi mở",
        ),
        growth_areas=(
            "Xây dựng một vài hệ thống và thói quen nhỏ để giữ vững những cam kết quan trọng",
            "Hoàn thành một dự án trước khi bắt đầu nhiều dự án mới",
            "Cân nhắc các lựa chọn bằng tiêu chí khách quan bên cạnh cảm nhận cá nhân",
            "Dành thời gian nghỉ ngơi thực sự để tránh kiệt sức",
        ),
        interpersonal=(
            "Bạn mang đến cho các mối quan hệ sự ấm áp, niềm vui và những lời khích lệ chân thành. "
            "Bạn có khả năng khiến người khác cảm thấy mình đặc biệt và có giá trị. "
            "Sự đồng cảm của bạn kết hợp trực giác về con người với sự tôn trọng sâu sắc bản sắc riêng của họ. "
            "Bạn trân trọng những mối quan hệ cho phép cả hai cùng lớn lên."
        ),
    ),
    "ISTJ": TypeProfile(
        title_vi="Người Gìn Giữ",
        title_en="The Steward",
        tagline="Đáng tin cậy, chu đáo, và là nền móng vững chắc cho mọi người.",
        core_drivers=(
            "Bạn được thúc đẩy bởi tinh thần trách nhiệm và mong muốn làm mọi việc một cách đúng đắn. "
            "Bạn tin rằng thế giới vận hành tốt nhất khi mỗi người giữ lời hứa và làm tròn bổn phận của mình. "
            "Sự ổn định, chính trực và đáng tin cậy là những giá trị cốt lõi. "
            "Bạn tìm thấy ý nghĩa trong việc gìn giữ những điều tốt đẹp đã được thời gian kiểm chứng."
        ),
        cognitive_processing=(
            "Cảm nhận hướng nội lưu giữ một kho kinh nghiệm chi tiết, giúp bạn đối chiếu hiện tại với những gì đã từng hiệu quả. "
            "Tư duy hướng ngoại sắp xếp công việc thành những quy trình rõ ràng, có thể kiểm chứng. "
            "Bạn xử lý thông tin một cách cẩn trọng và có hệ thống, kiểm tra kỹ trước khi đi đến kết luận."
        ),
        strengths=(
            "Đáng tin cậy và luôn giữ cam kết",
            "Chú ý đến chi tiết và độ chính xác",
            "Tổ chức và quản lý công việc hiệu quả",
            "Kiên nhẫn và bền bỉ",
        ),
        growth_areas=(
            "Mở lòng với những cách làm mới, xem chúng như những thử nghiệm có kiểm soát",
            "Bày tỏ cảm xúc và giá trị cá nhân nhiều hơn với những người thân",
            "Linh hoạt hơn khi hoàn cảnh thay đổi",
            "Xem nghỉ ngơi cũng là một trách nhiệm với chính mình",
        ),
        interpersonal=(
            "Bạn thể hiện tình cảm qua sự hiện diện ổn định và những hành động thiết thực: có mặt khi cần, nhớ những điều quan trọng, giữ trọn lời hứa. "
            "Bạn trân trọng sự trung thực và nhất quán trong các mối quan hệ. "
            "Bạn có thể không thể hiện cảm xúc rầm rộ, nhưng lòng trung thành của bạn rất sâu. "
            "Những người thân của bạn biết họ luôn có thể dựa vào bạn."
        ),
    ),
    "ISFJ": TypeProfile(
        title_vi="Người Che Chở",
        title_en="The Protector",
        tagline="Âm thầm chăm sóc, tận tụy và tinh tế với từng người xung quanh.",
        core_drivers=(
            "Bạn được thúc đẩy bởi mong muốn chăm sóc và bảo vệ những người mình yêu thương. "
            "Bạn nhìn thế giới qua những mối gắn kết, truyền thống và trách nhiệm dành cho nhau. "
            "Sự an toàn, hòa thuận và lòng biết ơn là những giá trị bạn trân quý. "
            "Bạn tìm thấy ý nghĩa trong những hành động nhỏ làm cuộc sống của người khác tốt đẹp hơn."
        ),
        cognitive_processing=(
            "Cảm nhận hướng nội giúp bạn ghi nhớ chi tiết về con người — sở thích, thói quen, những điều họ cần. "
            "Cảm xúc hướng ngoại giúp bạn cảm nhận và đáp ứng nhu cầu cảm xúc của người khác. "
            "Bạn xử lý thông tin bằng cách liên hệ với kinh nghiệm trước đây và xem nó ảnh hưởng thế nào đến mọi người."
        ),
        strengths=(
            "Tận tâm, chu đáo và để ý đến người khác",
            "Đáng tin cậy và có trách nhiệm",
            "Ghi nhớ những chi tiết quan trọng với người khác",
            "Kiên nhẫn và ổn định",
        ),
        growth_areas=(
            "Nói lên nhu cầu và giới hạn của chính mình",
            "Đón nhận thay đổi và những khả năng mới mà không lo lắng quá mức",
            "Ghi nhận giá trị của bản thân, không chỉ qua việc giúp đỡ người khác",
            "Phân tích vấn đề một cách khách quan khi cần đưa ra quyết định khó",
        ),
        interpersonal=(
            "Bạn là người mà mọi người tìm đến khi cần sự an ủi và hỗ trợ thiết thực. "
            "Bạn nhớ những chi tiết nhỏ và biến chúng thành những cử chỉ quan tâm đầy ý nghĩa. "
            "Sự đồng cảm của bạn thể hiện qua những hành động chăm sóc cụ thể. "
            "Hãy nhớ rằng nhận lại sự chăm sóc cũng quan trọng như trao đi."
        ),
    ),
    "ESTJ": TypeProfile(
        title_vi="Nhà Tổ Chức",
        title_en="The Organizer",
        tagline="Mang lại trật tự, sự rõ ràng và những kết quả đáng tin cậy.",
        core_drivers=(
            "Bạn được thúc đẩy bởi mong muốn làm cho mọi thứ vận hành hiệu quả và công bằng. "
            "Bạn nhìn thế giới qua lăng kính của trách nhiệm, tiêu chuẩn và kết quả. "
            "Bạn tin rằng một cộng đồng vững mạnh khi mỗi người làm tròn vai trò của mình. "
            "Trung thực, chăm chỉ và đáng tin cậy là những giá trị bạn sống cùng mỗi ngày."
        ),
        cognitive_processing=(
            "Tư duy hướng ngoại giúp bạn nhanh chóng tổ chức con người và nguồn lực để đạt được mục tiêu. "
            "Cảm nhận hướng nội cung cấp nền tảng kinh nghiệm và những quy trình đã được kiểm chứng. "
            "Bạn xử lý thông tin một cách thực tế: điều gì đã hiệu quả, điều gì cần làm, và ai sẽ làm."
        ),
        strengths=(
            "Năng lực tổ chức và quản lý xuất sắc",
            "Quyết đoán và rõ ràng",
            "Đáng tin cậy, luôn giữ cam kết",
            "Thẳng thắn và công bằng",
        ),
        growth_areas=(
            "Lắng nghe những ý tưởng chưa được kiểm chứng trước khi đánh giá chúng",
            "Nhận ra và bày tỏ những cảm xúc, giá trị cá nhân của mình",
            "Linh hoạt khi người khác có cách làm khác mình",
            "Ghi nhận cả nỗ lực và cảm xúc của người khác, không chỉ kết quả",
        ),
        interpersonal=(
            "Bạn thể hiện sự quan tâm bằng cách đảm bảo mọi người được chăm lo chu đáo — có kế hoạch, có nguồn lực, có sự ổn định. "
            "Bạn giao tiếp thẳng thắn và trân trọng sự rõ ràng. "
            "Bạn trung thành và luôn bảo vệ những người mình quan tâm. "
            "Khi bạn dành thêm thời gian lắng nghe cảm xúc, các mối quan hệ của bạn sẽ ngày càng sâu sắc."
        ),
    ),
    "ESFJ": TypeProfile(
        title_vi="Người Gắn Kết",
        title_en="The Harmonizer",
        tagline="Tạo nên sự ấm áp và gắn bó cho mọi cộng đồng mình thuộc về.",
        core_drivers=(
            "Bạn được thúc đẩy bởi mong muốn tạo ra sự hòa hợp và chăm lo cho cộng đồng. "
            "Bạn nhìn thế giới qua những mối quan hệ và trách nhiệm chung. "
            "Lòng hiếu khách, sự chu đáo và tinh thần đóng góp là những giá trị cốt lõi của bạn. "
            "Bạn tìm thấy niềm vui khi mọi người xung quanh cảm thấy được chào đón và gắn kết."
        ),
        cognitive_processing=(
            "Cảm xúc hướng ngoại giúp bạn đọc được bầu không khí và nhu cầu của mọi người, rồi hành động để đáp ứng chúng. "
            "Cảm nhận hướng nội lưu giữ kinh nghiệm về những gì đã từng khiến mọi người cảm thấy tốt hơn. "
            "Bạn xử lý thông tin bằng cách xem nó tác động thế nào đến con người, dựa trên những điều bạn đã biết."
        ),
        strengths=(
            "Ấm áp, thân thiện và giỏi kết nối",
            "Chu đáo với nhu cầu thực tế của người khác",
            "Có trách nhiệm và đáng tin cậy",
            "Xây dựng tinh thần cộng đồng",
        ),
        growth_areas=(
            "Phân biệt giữa giúp đỡ và gánh vác thay người khác",
            "Đánh giá vấn đề một cách khách quan bên cạnh việc cân nhắc cảm xúc",
            "Đón nhận những ý tưởng và thay đổi mới",
            "Ghi nhận giá trị của bản thân, độc lập với sự công nhận từ người khác",
        ),
        interpersonal=(
            "Bạn là người tổ chức những buổi họp mặt, nhớ ngày sinh nhật và hỏi thăm khi ai đó gặp khó khăn. "
            "Sự đồng cảm của bạn rất chủ động và thiết thực. "
            "Bạn trân trọng sự hòa thuận và nỗ lực gìn giữ nó. "
            "Hãy nhớ rằng những bất đồng được nói ra với sự tôn trọng cũng có thể làm mối quan hệ khỏe mạnh hơn."
        ),
    ),
    "ISTP": TypeProfile(
        title_vi="Nghệ Nhân Kỹ Thuật",
        title_en="The Craftsperson",
        tagline="Hiểu mọi thứ vận hành ra sao, và giữ bình tĩnh khi mọi thứ xáo trộn.",
        core_drivers=(
            "Bạn được thúc đẩy bởi sự tò mò về cách mọi thứ vận hành và mong muốn được tự do hành động theo cách của mình. "
            "Bạn nhìn thế giới như một tập hợp những cơ chế có thể hiểu được, sửa chữa được và cải tiến được. "
            "Sự độc lập, hiệu quả và năng lực thực tế là những giá trị cốt lõi. "
            "Bạn thấy thỏa mãn khi giải quyết được một vấn đề cụ thể bằng cả đôi tay lẫn trí óc."
        ),
        cognitive_processing=(
            "Tư duy hướng nội phân tích nguyên lý vận hành của sự vật một cách chính xác. "
            "Cảm nhận hướng ngoại giúp bạn nhạy bén với môi trường thực tế và phản ứng nhanh trước thay đổi. "
            "Bạn xử lý thông tin bằng cách quan sát, thử nghiệm trực tiếp và điều chỉnh liên tục."
        ),
        strengths=(
            "Giải quyết vấn đề thực tế xuất sắc",
            "Bình tĩnh trong khủng hoảng",
            "Linh hoạt và thích nghi nhanh",
            "Kỹ năng thực hành và kỹ thuật vững vàng",
        ),
        growth_areas=(
            "Chia sẻ suy nghĩ và cảm xúc với người thân, kể cả khi điều đó không cần thiết về mặt thực tế",
            "Lập kế hoạch dài hạn cho những mục tiêu thực sự quan trọng",
            "Để ý đến tác động cảm xúc của hành động mình lên người khác",
            "Duy trì cam kết ngay cả khi hứng thú ban đầu đã giảm",
        ),
        interpersonal=(
            "Bạn thể hiện sự quan tâm qua hành động cụ thể: sửa giúp, hỗ trợ khi cần, có mặt khi có sự cố. "
            "Bạn tôn trọng không gian riêng của người khác và mong đợi điều tương tự. "
            "Bạn trân trọng những mối quan hệ không có áp lực hay kịch tính. "
            "Những người thân thiết biết bạn là chỗ dựa bình tĩnh và đáng tin cậy trước mọi chuyện."
        ),
    ),
    "ISFP": TypeProfile(
        title_vi="Người Nghệ Sĩ",
        title_en="The Artist",
        tagline="Sống trọn vẹn từng khoảnh khắc, và thể hiện vẻ đẹp theo cách riêng.",
        core_drivers=(
            "Bạn được thúc đẩy bởi mong muốn sống chân thật với bản thân và trải nghiệm cuộc sống một cách trọn vẹn. "
            "Bạn nhìn thế giới với sự nhạy cảm sâu sắc trước cái đẹp, cảm xúc và giá trị. "
            "Tự do, chân thành và lòng tốt là những giá trị cốt lõi của bạn. "
            "Bạn tìm thấy ý nghĩa trong việc thể hiện bản thân và mang điều tốt đẹp đến cho người khác."
        ),
        cognitive_processing=(
            "Cảm xúc hướng nội là trung tâm giá trị, giúp bạn biết rõ điều gì là đúng với mình. "
            "Cảm nhận hướng ngoại giúp bạn cảm nhận tinh tế màu sắc, âm thanh, chất liệu và từng khoảnh khắc hiện tại. "
            "Bạn xử lý thông tin qua trải nghiệm trực tiếp và cảm nhận cá nhân."
        ),
        strengths=(
            "Nhạy cảm thẩm mỹ và sáng tạo",
            "Chân thành và tốt bụng",
            "Sống trọn trong hiện tại, linh hoạt",
            "Tôn trọng sự khác biệt",
        ),
        growth_areas=(
            "Lập kế hoạch cho những mục tiêu dài hạn thực sự quan trọng với bạn",
            "Bày tỏ quan điểm và nhu cầu, kể cả khi điều đó có thể dẫn đến bất đồng",
            "Đón nhận góp ý như một cơ hội để phát triển",
            "Tổ chức công việc có hệ thống hơn khi tình huống đòi hỏi",
        ),
        interpersonal=(
            "Bạn mang đến cho các mối quan hệ sự dịu dàng, chấp nhận và tôn trọng. "
            "Bạn thể hiện tình cảm qua hành động và những cử chỉ tinh tế hơn là lời nói. "
            "Bạn trân trọng sự chân thực và không thoải mái với sự giả tạo. "
            "Khi bạn chia sẻ thế giới nội tâm phong phú của mình, người khác sẽ nhận ra chiều sâu của bạn."
        ),
    ),
    "ESTP": TypeProfile(
        title_vi="Người Hành Động",
        title_en="The Dynamo",
        tagline="Nắm bắt cơ hội ngay lập tức, và biến thử thách thành trải nghiệm.",
        core_drivers=(
            "Bạn được thúc đẩy bởi sự hứng khởi trước hành động và những trải nghiệm thực tế. "
            "Bạn nhìn thế giới như một sân khấu đầy cơ hội cần được nắm bắt ngay lúc này. "
            "Tự do, hiệu quả và sự thẳng thắn là những giá trị cốt lõi của bạn. "
            "Bạn tin vào việc học qua làm và giải quyết vấn đề ngay khi nó xuất hiện."
        ),
        cognitive_processing=(
            "Cảm nhận hướng ngoại giúp bạn nhận ra nhanh chóng mọi thay đổi trong môi trường và phản ứng tức thì. "
            "Tư duy hướng nội giúp bạn phân tích tình huống một cách logic để tìm ra giải pháp hiệu quả. "
            "Bạn xử lý thông tin qua quan sát trực tiếp và hành động."
        ),
        strengths=(
            "Phản ứng nhanh và quyết đoán",
            "Giải quyết vấn đề thực tế",
            "Giao tiếp và thuyết phục tốt",
            "Thích nghi linh hoạt",
        ),
        growth_areas=(
            "Cân nhắc hệ quả dài hạn trước khi hành động",
            "Để ý đến cảm xúc của người khác trong giao tiếp",
            "Kiên nhẫn với những dự án cần thời gian để thành quả",
            "Dành thời gian lắng lại để suy ngẫm về bản thân",
        ),
        interpersonal=(
            "Bạn mang đến năng lượng, sự hài hước và tinh thần phiêu lưu cho các mối quan hệ. "
            "Bạn thể hiện sự quan tâm bằng hành động thiết thực và sự hiện diện. "
            "Bạn trân trọng sự thẳng thắn và không thích vòng vo. "
            "Khi kết hợp sự sôi nổi với khả năng lắng nghe, bạn trở thành một người bạn đồng hành tuyệt vời."
        ),
    ),
    "ESFP": TypeProfile(
        title_vi="Người Lan Tỏa Niềm Vui",
        title_en="The Enthusiast",
        tagline="Mang lại sức sống và niềm vui cho mọi khoảnh khắc.",
        core_drivers=(
            "Bạn được thúc đẩy bởi niềm vui sống và mong muốn chia sẻ nó với mọi người. "
            "Bạn nhìn thế giới như một nơi đầy những trải nghiệm đáng được tận hưởng. "
            "Sự ấm áp, tự do và chân thành là những giá trị cốt lõi của bạn. "
            "Bạn tìm thấy ý nghĩa khi khiến người khác mỉm cười và cảm thấy được trân trọng."
        ),
        cognitive_processing=(
            "Cảm nhận hướng ngoại giúp bạn sống trọn vẹn trong hiện tại, nhạy bén với con người và môi trường. "
            "Cảm xúc hướng nội giúp bạn biết điều gì thực sự có ý nghĩa với mình và với người khác. "
            "Bạn xử lý thông tin qua trải nghiệm trực tiếp và cảm nhận cá nhân."
        ),
        strengths=(
            "Nhiệt tình, vui vẻ và lan tỏa năng lượng",
            "Thấu hiểu và quan tâm đến người khác",
            "Linh hoạt, thích nghi nhanh",
            "Thực tế và giỏi xử lý vấn đề tức thời",
        ),
        growth_areas=(
            "Lập kế hoạch cho tương lai bên cạnh việc tận hưởng hiện tại",
            "Cân nhắc quyết định bằng những tiêu chí khách quan",
            "Đối diện với những cảm xúc khó khăn thay vì né tránh",
            "Duy trì cam kết với các mục tiêu dài hạn",
        ),
        interpersonal=(
            "Bạn mang đến cho các mối quan hệ sự ấm áp, niềm vui và tính tự nhiên. "
            "Bạn để ý đến người khác và biết cách khiến họ cảm thấy thoải mái. "
            "Sự đồng cảm của bạn thể hiện qua sự hiện diện và những hành động hỗ trợ thiết thực. "
            "Bạn trân trọng những mối quan hệ chân thành và vui vẻ."
        ),
    ),
}
