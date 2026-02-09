import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart';

class ContactUsPage extends StatefulWidget {
  const ContactUsPage({super.key});

  @override
  State<ContactUsPage> createState() => _ContactUsPageState();
}

class _ContactUsPageState extends State<ContactUsPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _emailController = TextEditingController();
  final _subjectController = TextEditingController();
  final _contentController = TextEditingController();
  
  String _messageType = 'General message';
  bool _isSending = false;

  final Map<String, List<String>> _types = {
    'en': ['Query', 'Complaint', 'Cooperation', 'Error in the App', 'Advice', 'General message'],
    'ar': ['استفسار', 'شكوى', 'تعاون', 'خطأ في التطبيق', 'نصيحة', 'رسالة عامة'],
  };

  final Map<String, String> _typeValues = {
    'استفسار': 'Query',
    'شكوى': 'Complaint',
    'تعاون': 'Cooperation',
    'خطأ في التطبيق': 'Error in the App',
    'نصيحة': 'Advice',
    'رسالة عامة': 'General message',
  };

  Future<void> _submitForm(bool isAr) async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSending = true);

    try {
      final response = await http.post(
        Uri.parse('https://saghalive.com/api/contact'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': _nameController.text,
          'phone': _phoneController.text,
          'email': _emailController.text,
          'type': isAr ? (_typeValues[_messageType] ?? 'General message') : _messageType,
          'subject': _subjectController.text,
          'content': _contentController.text,
          'source': 'Mobile',
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        _showSuccessDialog(isAr);
      } else {
        _showErrorSnackBar(isAr ? "فشل الإرسال. يرجى المحاولة لاحقاً." : "Failed to send. Please try again later.");
      }
    } catch (e) {
      _showErrorSnackBar(isAr ? "خطأ في الاتصال بالخادم." : "Network error. Please check your connection.");
    } finally {
      if (mounted) setState(() => _isSending = false);
    }
  }

  void _showSuccessDialog(bool isAr) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF111111),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20), side: const BorderSide(color: Color(0xFFD4AF37), width: 0.5)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.check_circle_outline, color: Colors.green, size: 80),
            const SizedBox(height: 20),
            Text(
              isAr ? "شكراً لك!" : "Thank You!",
              style: GoogleFonts.outfit(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 10),
            Text(
              isAr 
                ? "لقد تم إرسال رسالتك بنجاح. سنقوم بمراجعتها والرد عليك في أقرب وقت ممكن."
                : "Your message has been successfully submitted. We will review it and get back to you soon.",
              textAlign: TextAlign.center,
              style: GoogleFonts.outfit(color: Colors.white70, fontSize: 14),
            ),
            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pop(ctx); // Close Dialog
                  Navigator.pop(context); // Close Page
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFD4AF37),
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: Text(isAr ? "إغلاق" : "Close", style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showErrorSnackBar(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg), backgroundColor: Colors.redAccent));
  }

  @override
  Widget build(BuildContext context) {
    // Note: I'm assuming there's a LocaleProvider or similar based on shared context.
    // If not found, I'll fallback to basic check.
    dynamic provider;
    try {
      provider = Provider.of<dynamic>(context);
    } catch(_) {}
    
    final bool isAr = provider?.locale?.languageCode == 'ar';
    final isDark = Theme.of(context).brightness == Brightness.dark;

    if (isAr && !_types['ar']!.contains(_messageType) && !_typeValues.containsKey(_messageType)) {
       _messageType = _types['ar']!.last;
    } else if (!isAr && !_types['en']!.contains(_messageType)) {
       _messageType = _types['en']!.last;
    }

    return Scaffold(
      backgroundColor: isDark ? const Color(0xFF080808) : Colors.white,
      appBar: AppBar(
        title: Text(isAr ? "اتصل بنا" : "Contact Us", style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                isAr 
                  ? "يمكنك التواصل معنا بخصوص اقتراحاتك، شكواك أو نصائحك حول التطبيق عبر هذه الشاشة."
                  : "You can contact us with your suggestions, complaints or advices about the App using this screen.",
                style: GoogleFonts.outfit(color: isDark ? Colors.white60 : Colors.black54, fontSize: 14),
                textAlign: isAr ? TextAlign.right : TextAlign.left,
                textDirection: isAr ? TextDirection.rtl : TextDirection.ltr,
              ),
              const SizedBox(height: 30),
              _buildField("name", _nameController, isAr, isDark, required: true),
              _buildField("phone", _phoneController, isAr, isDark),
              _buildField("email", _emailController, isAr, isDark, required: true, isEmail: true),
              
              _buildLabel(isAr ? "نوع الرسالة" : "Message Type", isAr, isDark),
              DropdownButtonFormField<String>(
                value: _messageType,
                dropdownColor: isDark ? const Color(0xFF1A1A1A) : Colors.white,
                style: GoogleFonts.outfit(color: isDark ? Colors.white : Colors.black),
                decoration: _fieldDecoration("", isAr, isDark),
                items: _types[isAr ? 'ar' : 'en']!.map((t) => DropdownMenuItem(value: t, child: Text(t))).toList(),
                onChanged: (v) => setState(() => _messageType = v!),
              ),
              const SizedBox(height: 20),
              
              _buildField("subject", _subjectController, isAr, isDark, required: true),
              _buildField("content", _contentController, isAr, isDark, required: true, maxLines: 5),
              
              const SizedBox(height: 40),
              SizedBox(
                width: double.infinity,
                height: 55,
                child: ElevatedButton(
                  onPressed: _isSending ? null : () => _submitForm(isAr),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFD4AF37),
                    foregroundColor: Colors.black,
                    disabledBackgroundColor: Colors.grey.withOpacity(0.3),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    elevation: 5,
                    shadowColor: const Color(0xFFD4AF37).withOpacity(0.4),
                  ),
                  child: _isSending 
                    ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2))
                    : Text(isAr ? "إرسال" : "Send", style: GoogleFonts.outfit(fontSize: 18, fontWeight: FontWeight.bold)),
                ),
              ),
              const SizedBox(height: 50),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLabel(String label, bool isAr, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8, left: 4, right: 4),
      child: Text(
        label, 
        style: GoogleFonts.outfit(fontSize: 14, fontWeight: FontWeight.w600, color: isDark ? Colors.white70 : Colors.black87),
        textDirection: isAr ? TextDirection.rtl : TextDirection.ltr,
      ),
    );
  }

  Widget _buildField(String key, TextEditingController controller, bool isAr, bool isDark, {bool required = false, bool isEmail = false, int maxLines = 1}) {
    final labels = {
      "name": isAr ? "الأسم" : "Name",
      "phone": isAr ? "رقم الهاتف" : "Phone",
      "email": isAr ? "البريد الإلكتروني" : "Email",
      "subject": isAr ? "الموضوع" : "Subject",
      "content": isAr ? "المحتوى" : "Content",
    };

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLabel(labels[key]!, isAr, isDark),
        TextFormField(
          controller: controller,
          maxLines: maxLines,
          style: GoogleFonts.outfit(color: isDark ? Colors.white : Colors.black),
          textAlign: isAr ? TextAlign.right : TextAlign.left,
          textDirection: isAr ? TextDirection.rtl : TextDirection.ltr,
          validator: (v) {
            if (required && (v == null || v.isEmpty)) return isAr ? "هذا الحقل مطلوب" : "Required field";
            if (isEmail && v != null && v.isNotEmpty && !v.contains("@")) return isAr ? "البريد غير صحيح" : "Invalid email";
            return null;
          },
          decoration: _fieldDecoration("", isAr, isDark),
        ),
        const SizedBox(height: 20),
      ],
    );
  }

  InputDecoration _fieldDecoration(String hint, bool isAr, bool isDark) {
    return InputDecoration(
      hintText: hint,
      filled: true,
      fillColor: isDark ? const Color(0xFF141414) : Colors.grey[100],
      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: isDark ? BorderSide(color: Colors.white10, width: 1) : BorderSide.none),
      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Color(0xFFD4AF37), width: 1.5)),
      errorStyle: GoogleFonts.outfit(color: Colors.redAccent),
    );
  }
}
