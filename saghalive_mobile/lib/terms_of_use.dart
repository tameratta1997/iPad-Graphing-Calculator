import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class TermsOfUsePage extends StatelessWidget {
  const TermsOfUsePage({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final textColor = isDark ? Colors.white : Colors.black;
    final dimColor = isDark ? Colors.white70 : Colors.black87;

    return Scaffold(
      appBar: AppBar(
        title: Text("Terms of Use", style: GoogleFonts.outfit()),
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // English Section
            _buildHeader("Terms & Conditions", textColor),
            _buildText("Last Updated: 16-01-2026", dimColor, isItalic: true),
            const SizedBox(height: 10),
            _buildText("Welcome to SaghaLive. By accessing or using this website, you agree to the following Terms and Conditions.", dimColor),
            
            _buildSubHeader("1. Content Nature", textColor),
            _buildBullet("The website provides informational content only related to gold and silver prices and market analysis.", dimColor),
            _buildBullet("Content does not constitute financial or investment advice.", dimColor),

            _buildSubHeader("2. Accuracy of Information", textColor),
            _buildBullet("We strive to provide accurate and updated information but do not guarantee accuracy.", dimColor),
            _buildBullet("Prices may change based on market conditions.", dimColor),

            _buildSubHeader("3. Intellectual Property", textColor),
            _buildBullet("All content published on the website is owned by SaghaLive.", dimColor),
            _buildBullet("Unauthorized reproduction or redistribution is prohibited.", dimColor),

            _buildSubHeader("4. Limitation of Liability", textColor),
            _buildBullet("SaghaLive shall not be liable for financial losses resulting from reliance on published information.", dimColor),
            _buildBullet("Users access content at their own risk.", dimColor),

            _buildSubHeader("5. Advertising", textColor),
            _buildBullet("The website may display third-party advertisements.", dimColor),
            _buildBullet("SaghaLive is not responsible for advertised products or services.", dimColor),

            _buildSubHeader("6. User Conduct", textColor),
            _buildText("Users must not use the website unlawfully, attempt to breach security, or abuse contact forms or services.", dimColor),

            _buildSubHeader("7. External Links", textColor),
            _buildText("SaghaLive is not responsible for third-party websites linked from the platform.", dimColor),

            _buildSubHeader("8. Modifications", textColor),
            _buildText("Terms may be updated at any time. Continued use constitutes acceptance.", dimColor),

            _buildSubHeader("9. Governing Law", textColor),
            _buildText("These terms are governed by applicable laws without specific jurisdiction.", dimColor),

            _buildSubHeader("10. Contact", textColor),
            _buildText("For inquiries regarding these terms, please contact us via the Contact Us page.", dimColor),
            
            const Divider(height: 40),

            // Arabic Section
            _buildHeader("شروط الاستخدام", textColor, isRtl: true),
            _buildText("آخر تحديث: ١٦-٠١-٢٠٢٦", dimColor, isRtl: true, isItalic: true),
            const SizedBox(height: 10),
            _buildText("مرحبًا بك في موقع SaghaLive. باستخدامك لهذا الموقع، فإنك توافق على الالتزام بشروط الاستخدام التالية.", dimColor, isRtl: true),
            
            _buildSubHeader("١. طبيعة المحتوى", textColor, isRtl: true),
            _buildBullet("يقدم الموقع محتوى معلوماتي فقط عن أسعار الذهب والفضة والتحليلات السوقية.", dimColor, isRtl: true),
            _buildBullet("لا يُعد أي محتوى منشور نصيحة استثمارية أو توصية مالية.", dimColor, isRtl: true),

            _buildSubHeader("٢. دقة المعلومات", textColor, isRtl: true),
            _buildBullet("نسعى لتقديم معلومات دقيقة ومحدثة، دون ضمان خلوها من الأخطاء.", dimColor, isRtl: true),
            _buildBullet("الأسعار قابلة للتغيير وفقًا لحركة الأسواق المحلية والعالمية.", dimColor, isRtl: true),

            _buildSubHeader("٣. حقوق الملكية الفكرية", textColor, isRtl: true),
            _buildBullet("جميع المحتويات المنشورة على الموقع مملوكة لـ SaghaLive.", dimColor, isRtl: true),
            _buildBullet("يمنع نسخ أو إعادة نشر المحتوى دون إذن كتابي مسبق.", dimColor, isRtl: true),

            _buildSubHeader("٤. حدود المسؤولية", textColor, isRtl: true),
            _buildBullet("لا يتحمل الموقع أي مسؤولية عن خسائر مالية أو قرارات استثمارية ناتجة عن استخدام المعلومات المنشورة.", dimColor, isRtl: true),
            _buildBullet("استخدام المحتوى يتم على مسؤولية المستخدم.", dimColor, isRtl: true),

            _buildSubHeader("٥. الإعلانات", textColor, isRtl: true),
            _buildBullet("قد يحتوي الموقع على إعلانات من أطراف ثالثة.", dimColor, isRtl: true),
            _buildBullet("لا يتحمل SaghaLive مسؤولية محتوى الإعلانات أو الخدمات المعلن عنها.", dimColor, isRtl: true),

            _buildSubHeader("٦. سلوك المستخدم", textColor, isRtl: true),
            _buildText("يُمنع على المستخدم استخدام الموقع لأغراض غير قانونية أو محاولة اختراقه أو الإضرار به أو إساءة استخدام نماذج التواصل.", dimColor, isRtl: true),

            _buildSubHeader("٧. الروابط الخارجية", textColor, isRtl: true),
            _buildText("قد يحتوي الموقع على روابط لمواقع خارجية ولسنا مسؤولين عن محتواها أو سياساتها.", dimColor, isRtl: true),

            _buildSubHeader("٨. تعديل الشروط", textColor, isRtl: true),
            _buildText("يحتفظ الموقع بالحق في تعديل شروط الاستخدام في أي وقت، ويعد الاستمرار في الاستخدام موافقة على التعديلات.", dimColor, isRtl: true),

            _buildSubHeader("٩. القانون المعمول به", textColor, isRtl: true),
            _buildText("تخضع هذه الشروط للقوانين المعمول بها دون تحديد اختصاص قضائي بعينه.", dimColor, isRtl: true),

            _buildSubHeader("١٠. التواصل", textColor, isRtl: true),
            _buildText("لأي استفسار حول شروط الاستخدام، يرجى التواصل عبر صفحة اتصل بنا.", dimColor, isRtl: true),

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
