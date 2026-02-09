import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PrivacyPolicyPage extends StatelessWidget {
  const PrivacyPolicyPage({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final textColor = isDark ? Colors.white : Colors.black;
    final dimColor = isDark ? Colors.white70 : Colors.black87;

    return Scaffold(
      appBar: AppBar(
        title: Text("Privacy Policy", style: GoogleFonts.outfit()),
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // English Section
            _buildHeader("Privacy Policy", textColor),
            _buildText("Last Updated: 16-01-2026", dimColor, isItalic: true),
            const SizedBox(height: 10),
            _buildText("At SaghaLive, a platform specialized in gold and silver prices, precious metals market analysis, and updates, we are committed to protecting the privacy of our visitors. This policy explains how information is collected, used, and protected.", dimColor),
            
            _buildSubHeader("1. Information We Collect", textColor),
            _buildText("We may collect non-personal information such as:", dimColor),
            _buildBullet("IP address", dimColor),
            _buildBullet("Browser and device type", dimColor),
            _buildBullet("Operating system", dimColor),
            _buildBullet("Pages visited", dimColor),
            _buildBullet("Date and time of visits", dimColor),
            _buildText("Personal information is collected only when voluntarily provided, such as contacting us through forms or email.", dimColor),

            _buildSubHeader("2. How We Use Information", textColor),
            _buildBullet("Provide accurate gold and silver price updates", dimColor),
            _buildBullet("Improve market analysis and content", dimColor),
            _buildBullet("Enhance user experience", dimColor),
            _buildBullet("Analyze traffic and visitor behavior", dimColor),
            _buildBullet("Display relevant advertisements", dimColor),

            _buildSubHeader("3. Cookies", textColor),
            _buildText("SaghaLive uses local storage or cookies to store preferences, analyze performance, and improve services. You can manage these via your device settings.", dimColor),

            _buildSubHeader("4. Advertising Partners", textColor),
            _buildText("SaghaLive may use third-party services like Google Ads. Google uses cookies to serve ads based on your visits. You can opt out via: https://adssettings.google.com/", dimColor),

            _buildSubHeader("5. Data Sharing", textColor),
            _buildText("We do not sell personal data. Data may be shared with analytics partners (e.g., Google Analytics) or legal authorities if required by law.", dimColor),

            _buildSubHeader("6. Data Security", textColor),
            _buildText("We implement appropriate security measures and use industry-standard encryption (HTTPS) to safeguard your information.", dimColor),

            _buildSubHeader("7. User Rights", textColor),
            _buildText("Users have the right to request access, correction, or deletion of their personal data. Requests can be submitted via the Contact Us page and will be addressed within 30 days.", dimColor),

            _buildSubHeader("8. External Links", textColor),
            _buildText("SaghaLive may contain links to external sites. We are not responsible for their content or privacy practices.", dimColor),

            _buildSubHeader("9. User Consent", textColor),
            _buildText("By using SaghaLive, you consent to this Privacy Policy.", dimColor),

            _buildSubHeader("10. Policy Updates", textColor),
            _buildText("This policy may be updated at any time. Updates will be posted on this page.", dimColor),

            _buildSubHeader("11. Contact", textColor),
            _buildText("For privacy-related inquiries, please contact us via the Contact Us page.", dimColor),
            
            const Divider(height: 40),

            // Arabic Section
            _buildHeader("سياسة الخصوصية", textColor, isRtl: true),
            _buildText("آخر تحديث: ١٦-٠١-٢٠٢٦", dimColor, isRtl: true, isItalic: true),
            const SizedBox(height: 10),
            _buildText("في منصة SaghaLive، المتخصص في عرض أسعار الذهب والفضة، التحليلات السوقية، وأخبار المعادن الثمينة، نلتزم بحماية خصوصية زوارنا ونوضح في هذه الوثيقة كيفية جمع واستخدام وحماية المعلومات.", dimColor, isRtl: true),
            
            _buildSubHeader("١. المعلومات التي نقوم بجمعها", textColor, isRtl: true),
            _buildText("قد نقوم بجمع معلومات غير شخصية تشمل:", dimColor, isRtl: true),
            _buildBullet("عنوان بروتوكول الإنترنت (IP)", dimColor, isRtl: true),
            _buildBullet("نوع المتصفح والجهاز", dimColor, isRtl: true),
            _buildBullet("نظام التشغيل", dimColor, isRtl: true),
            _buildBullet("الصفحات التي تمت زيارتها", dimColor, isRtl: true),
            _buildBullet("وقت وتاريخ الزيارة", dimColor, isRtl: true),
            _buildText("كما نجمع معلومات شخصية فقط عند تقديمها طوعاً عبر نماذج الاتصال أوالبريد الإلكتروني.", dimColor, isRtl: true),

            _buildSubHeader("٢. كيفية استخدام المعلومات", textColor, isRtl: true),
            _buildBullet("عرض أسعار الذهب والفضة بدقة وتحديثها", dimColor, isRtl: true),
            _buildBullet("تحسين التحليلات والمحتوى السوقي", dimColor, isRtl: true),
            _buildBullet("تطوير تجربة المستخدم", dimColor, isRtl: true),
            _buildBullet("تحليل حركة الزوار لأغراض إحصائية", dimColor, isRtl: true),
            _buildBullet("عرض إعلانات مناسبة لاهتمامات الزوار", dimColor, isRtl: true),

            _buildSubHeader("٣. ملفات تعريف الارتباط (Cookies)", textColor, isRtl: true),
            _buildText("يستخدم التطبيق تقنيات التخزين المحلي لحفظ التفضيلات وتحسين الأداء. يمكنك تعطيلها عبر إعدادات جهازك.", dimColor, isRtl: true),

            _buildSubHeader("٤. الإعلانات وشركات الإعلان الخارجية", textColor, isRtl: true),
            _buildText("قد نستخدم خدمات مثل Google Ads التي تستخدم ملفات تعريف الارتباط لعرض إعلانات مخصصة. يمكنك إدارة ذلك عبر: https://adssettings.google.com/", dimColor, isRtl: true),

            _buildSubHeader("٥. مشاركة البيانات", textColor, isRtl: true),
            _buildText("لا نقوم ببيع البيانات الشخصية. قد تتم مشاركتها فقط مع شركاء التحليل أو الجهات القانونية عند الضرورة.", dimColor, isRtl: true),

            _buildSubHeader("٦. حماية المعلومات", textColor, isRtl: true),
            _buildText("نطبق إجراءات أمنية واستخدام تشفير HTTPS لحماية معلوماتك.", dimColor, isRtl: true),

            _buildSubHeader("٧. حقوق المستخدم", textColor, isRtl: true),
            _buildText("يحق للمستخدم طلب الوصول إلى بياناته أو تصحيحها أو حذفها عبر صفحة اتصل بنا، وسيتم الرد خلال ٣٠ يوماً.", dimColor, isRtl: true),

            _buildSubHeader("٨. الروابط الخارجية", textColor, isRtl: true),
            _buildText("لسنا مسؤولين عن سياسات الخصوصية أو محتوى المواقع الخارجية المرتبطة.", dimColor, isRtl: true),

            _buildSubHeader("٩. موافقة المستخدم", textColor, isRtl: true),
            _buildText("باستخدامك SaghaLive، فإنك توافق على سياسة الخصوصية هذه.", dimColor, isRtl: true),

            _buildSubHeader("١٠. تحديثات سياسة الخصوصية", textColor, isRtl: true),
            _buildText("قد نقوم بتحديث هذه السياسة في أي وقت، وسيتم نشر التحديثات على هذه الصفحة.", dimColor, isRtl: true),

            _buildSubHeader("١١. التواصل", textColor, isRtl: true),
            _buildText("للاستفسارات، يرجى التواصل عبر صفحة اتصل بنا.", dimColor, isRtl: true),

            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(String text, Color color, {bool isRtl = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 20),
      child: Text(text, textAlign: isRtl ? TextAlign.right : TextAlign.left, style: GoogleFonts.outfit(fontSize: 24, fontWeight: FontWeight.bold, color: color), textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr),
    );
  }

  Widget _buildSubHeader(String text, Color color, {bool isRtl = false}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.only(top: 20, bottom: 10),
      decoration: BoxDecoration(border: Border(bottom: BorderSide(color: color.withOpacity(0.1)))),
      child: Text(text, textAlign: isRtl ? TextAlign.right : TextAlign.left, style: GoogleFonts.outfit(fontSize: 18, fontWeight: FontWeight.bold, color: color), textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr),
    );
  }

  Widget _buildText(String text, Color color, {bool isRtl = false, bool isItalic = false}) {
    return SizedBox(
      width: double.infinity,
      child: Text(
        text, 
        textAlign: isRtl ? TextAlign.right : TextAlign.left, 
        style: GoogleFonts.outfit(fontSize: 14, color: color, fontStyle: isItalic ? FontStyle.italic : FontStyle.normal),
        textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr
      )
    );
  }

  Widget _buildBullet(String text, Color color, {bool isRtl = false}) {
    return Padding(
      padding: EdgeInsets.only(left: isRtl ? 0 : 20, right: isRtl ? 20 : 0, top: 5),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr,
        children: [
          Text("• ", style: TextStyle(color: color, fontSize: 16)),
          Expanded(child: Text(text, style: GoogleFonts.outfit(fontSize: 14, color: color), textDirection: isRtl ? TextDirection.rtl : TextDirection.ltr)),
        ],
      ),
    );
  }
}
