// Static copy shared by several views. Result-specific text comes from the API.

export const POLES = {
  E: 'Hướng ngoại',
  I: 'Hướng nội',
  S: 'Cảm nhận',
  N: 'Trực giác',
  T: 'Lý trí',
  F: 'Cảm xúc',
  J: 'Nguyên tắc',
  P: 'Linh hoạt',
};

export const POLES_EN = {
  E: 'Extraversion',
  I: 'Introversion',
  S: 'Sensing',
  N: 'Intuition',
  T: 'Thinking',
  F: 'Feeling',
  J: 'Judging',
  P: 'Perceiving',
};

// Site-wide footer (rendered by main.js, and inside the last landing section).
export const FOOTER_NOTE =
  'Tâm Đồ là công cụ giúp bạn soi chiếu và khám phá con người sâu thẳm bên trong mình, không phải là một chẩn đoán tâm lý lâm sàng.';

// Landing page copy, one entry per full-screen section.
export const LANDING = {
  // Labels for the side dot navigation, in section order.
  sections: ['Giới thiệu', 'Bốn chiều tính cách', 'Tám chức năng nhận thức'],
  heroTitle: 'Hiểu sâu hơn cách bạn nhìn, nghĩ và kết nối.',
  heroIntro:
    'Dựa trên công trình nền tảng về các Loại hình Tâm lý của nhà triết học & bác sĩ tâm thần Carl Jung, MBTI không phải là chiếc hộp để dán nhãn hay giới hạn bản thân. Đây là tấm gương giúp bạn soi chiếu cách tâm trí mình tiếp nhận thế giới, đưa ra quyết định và vận hành nguồn năng lượng nội tại mỗi ngày.',
  dimsIntro:
    'Mô hình MBTI nhìn nhận con người qua bốn chiều kích tâm lý tự nhiên. Trong mỗi chiều, bạn đều sở hữu và sử dụng cả hai xu hướng — không có chiều nào là tốt hơn hay kém hơn bên nào cả. Bài trắc nghiệm này đơn giản là giúp bạn nhận diện xem tâm trí mình thường vô thức ngả về bên nào nhiều hơn.',
  functionsIntro:
    "Dưới góc nhìn của Carl Jung, tâm trí chúng ta vận hành thông qua tám Chức năng Nhận thức (Cognitive Functions). Tùy thuộc vào việc các chức năng này hướng ra ngoài hay hướng vào trong, chúng xếp thành một 'ngăn xếp' (stack) độc nhất — từ chức năng chủ đạo chi phối suy nghĩ đến chức năng tiềm ẩn cần được thấu hiểu.",
};

export const DICHOTOMIES = [
  {
    key: 'EI',
    theme: 'Nguồn năng lượng',
    question:
      'Năng lượng của bạn thường bừng sáng khi tương tác với thế giới bên ngoài, hay được chữa lành khi trở về với không gian tĩnh lặng bên trong?',
  },
  {
    key: 'SN',
    theme: 'Tiếp nhận thông tin',
    question:
      'Tâm trí bạn ưu tiên tin vào những dữ kiện thực tế mắt thấy tai nghe, hay thường nhạy bén với những ý nghĩa ẩn giấu và khả năng của tương lai?',
  },
  {
    key: 'TF',
    theme: 'Ra quyết định',
    question:
      'Khi đứng trước một lựa chọn quan trọng, điều gì nắm quyền quyết định: sự nhất quán khách quan của logic, hay tiếng nói thấu cảm từ trái tim?',
  },
  {
    key: 'JP',
    theme: 'Tiếp cận cuộc sống',
    question:
      'Bạn cảm thấy bình yên khi mọi thứ được lập kế hoạch rõ ràng, hay cảm thấy tự do khi sẵn sàng ứng biến theo dòng chảy tự nhiên?',
  },
];

export const FUNCTIONS = [
  { code: 'Ni', en: 'Introverted Intuition', vi: 'Trực giác hướng nội', desc: 'Lắng đọng tín hiệu thành nhận thức sâu sắc về xu hướng tương lai.' },
  { code: 'Ne', en: 'Extraverted Intuition', vi: 'Trực giác hướng ngoại', desc: 'Nhìn ra muôn vàn khả năng và mối liên kết mới trong thế giới xung quanh.' },
  { code: 'Si', en: 'Introverted Sensing', vi: 'Cảm nhận hướng nội', desc: 'Đối chiếu thực tại với kho tàng trải nghiệm và ký ức đã lưu giữ.' },
  { code: 'Se', en: 'Extraverted Sensing', vi: 'Cảm nhận hướng ngoại', desc: 'Chìm đắm trọn vẹn vào thực tại qua 5 giác quan và phản ứng tức thì.' },
  { code: 'Ti', en: 'Introverted Thinking', vi: 'Tư duy hướng nội', desc: 'Xây dựng hệ thống logic nội tại chính xác và nhất quán đến từng chi tiết.' },
  { code: 'Te', en: 'Extraverted Thinking', vi: 'Tư duy hướng ngoại', desc: 'Tổ chức thế giới bên ngoài theo mục tiêu, tính hiệu quả và bằng chứng.' },
  { code: 'Fi', en: 'Introverted Feeling', vi: 'Cảm xúc hướng nội', desc: 'Đánh giá mọi việc dựa trên hệ giá trị cá nhân sâu sắc và sự chân thật.' },
  { code: 'Fe', en: 'Extraverted Feeling', vi: 'Cảm xúc hướng ngoại', desc: 'Hướng tới sự hòa hợp tập thể, nhạy bén với cảm xúc của người xung quanh.' },
];

// ~7 seconds per item, rounded to whole minutes.
export const LENGTHS = [
  { count: 25, minutes: 3, label: 'Nhanh' },
  { count: 50, minutes: 6, label: 'Cân bằng', recommended: true },
  { count: 75, minutes: 9, label: 'Chi tiết' },
  { count: 100, minutes: 12, label: 'Toàn diện' },
];

// Left-to-right visual order; keyboard 1–7 follows the same order.
export const LIKERT = [
  { score: 3, label: 'Rất đồng ý' },
  { score: 2, label: 'Đồng ý' },
  { score: 1, label: 'Hơi đồng ý' },
  { score: 0, label: 'Trung lập' },
  { score: -1, label: 'Hơi không đồng ý' },
  { score: -2, label: 'Không đồng ý' },
  { score: -3, label: 'Rất không đồng ý' },
];

export const PROFILE_TABS = [
  ['core_drivers', 'Động lực & Thế giới quan cốt lõi', 'Core Psychological Drivers'],
  ['cognitive_functions', 'Chức năng nhận thức & Xử lý thông tin', 'Cognitive Functions'],
  ['strengths_growth', 'Điểm mạnh & Góc nhìn phát triển', 'Strengths & Growth Mindset'],
  ['interpersonal', 'Phong cách tương tác & Thấu cảm', 'Interpersonal Dynamics'],
];
