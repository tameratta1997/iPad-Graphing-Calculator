import 'dart:async';
import 'dart:ui' as ui;
import 'dart:convert';
import 'dart:math' as math;
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

import 'dart:io'; // Added for HttpOverrides
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'privacy_policy.dart';
import 'terms_of_use.dart';
import 'contact_us.dart';




void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppProvider(prefs)),
      ],
      child: const SaghaLiveApp(),
    ),
  );
}

// ... (Imports stay same)

// --- Theme Constants ---
class AppColors {
  // Dark Mode
  static const Color bgDark = Color(0xFF050505);
  static const Color cardBg = Color(0xFF111111);
  static const Color textMain = Colors.white;
  
  // Light Mode
  static const Color bgLight = Color(0xFFF8F9FA); // Off-white
  static const Color cardBgLight = Color(0xFFFFFFFF);
  static const Color textMainLight = Color(0xFF1A1A1A); // Dark Grey

  // Shared
  static const Color primary = Color(0xFFD4AF37);
  static const Color primaryLight = Color(0xFFF9E27D);
  static const Color textDim = Color(0xFF94A3B8); // Slate 400 works on both usually, or darken for light mode
  static const Color silver = Color(0xFFC0C0C0);
  static const Color success = Color(0xFF4ADE80);
  static const Color error = Color(0xFFEF4444);
}

class PulseDot extends StatefulWidget {
  const PulseDot({super.key});

  @override
  State<PulseDot> createState() => _PulseDotState();
}

class _PulseDotState extends State<PulseDot> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(duration: const Duration(seconds: 1), vsync: this)..repeat(reverse: true);
    _animation = Tween<double>(begin: 4.0, end: 10.0).animate(_controller);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Container(
          width: 8, height: 8,
          decoration: BoxDecoration(
            color: AppColors.success,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: AppColors.success.withOpacity(0.4),
                blurRadius: _animation.value,
                spreadRadius: _animation.value / 2,
              )
            ],
          ),
        );
      },
    );
  }
}

class AppProvider with ChangeNotifier {
  final SharedPreferences prefs;
  AppProvider(this.prefs) {
    _locale = Locale(prefs.getString('lang') ?? 'en');
    _isDark = prefs.getBool('isDark') ?? true; // Default Dark
    _startClock();
  }

  int _userOffset = 7200; // Default UTC+2
  String _userCity = "Cairo";
  String get userCity => _userCity;
  String _userTimezone = "Africa/Cairo";
  DateTime _currentTime = DateTime.now();
  DateTime get currentTime => _currentTime;
  Timer? _clockTimer;

  Locale _locale = const Locale('en');
  Locale get locale => _locale;
  
  bool _isDark = true;
  bool get isDark => _isDark;

  // ... (Data properties same)
  Map<String, dynamic>? _data;
  Map<String, dynamic>? get data => _data;
  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String _activeMetal = 'gold';
  String get activeMetal => _activeMetal;
  
  // Chart Data
  List<FlSpot> _chartData = [];
  List<FlSpot> get chartData => _chartData;
  List<String> _chartLabels = [];
  List<String> get chartLabels => _chartLabels;
  String _chartRange = '1m';
  String get chartRange => _chartRange;
  
  // Analysis Data
  Map<String, dynamic>? _analysisData;
  Map<String, dynamic>? get analysisData => _analysisData;

  // Error Handling
  String? _errorMessage;
  String? get errorMessage => _errorMessage;

  String _currentCurrency = 'EGP';
  String get currentCurrency => _currentCurrency;
  
  Map<String, double> _conversionRates = {
    'EGP': 1.0,
    'SAR': 0.078,
    'AED': 0.076,
  };
  Map<String, double> get conversionRates => _conversionRates;

  void setLocale(String langCode) {
    _locale = Locale(langCode);
    prefs.setString('lang', langCode);
    notifyListeners();
  }
  
  void toggleTheme() {
    _isDark = !_isDark;
    prefs.setBool('isDark', _isDark);
    notifyListeners();
  }

  // ... (setActiveMetal, setChartRange, fetchHistory, fetchData same)
  void setActiveMetal(String metal) {
    _activeMetal = metal;
    fetchHistory();
    notifyListeners();
  }

  void setChartRange(String range) {
    _chartRange = range;
    fetchHistory();
    notifyListeners();
  }

  Future<void> fetchHistory() async {
    try {
      final response = await http
          .get(Uri.parse('https://saghalive.com/api/history?metal=$_activeMetal&period=$_chartRange'))
          .timeout(const Duration(seconds: 15));
      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        final List<dynamic> points = json['data'];
        
        _chartLabels = points.map((p) {
          final dt = DateTime.fromMillisecondsSinceEpoch(p['t'] as int);
          if (_chartRange == '24h' || _chartRange == 'hour') {
            return "${dt.hour}:${dt.minute.toString().padLeft(2, '0')}";
          } else if (_chartRange == '1y') {
            return DateFormat('MMM').format(dt);
          } else {
            return "${dt.month}/${dt.day}";
          }
        }).toList();

        _chartData = points.asMap().entries.map((e) {
          final point = e.value;
          double y = (point['y'] as num).toDouble();
          return FlSpot(e.key.toDouble(), y);
        }).toList();
        
        if (json['analysis'] != null) {
          _analysisData = json['analysis'];
        }
      }
    } catch (e) {
      debugPrint("Error fetching history: $e");
       // Don't override main error if history fails
    }
    notifyListeners();
  }

  Future<void> fetchData() async {
    _isLoading = true;
    _errorMessage = null; // Reset error
    notifyListeners();
    try {
      final response = await http
          .get(Uri.parse('https://saghalive.com/api/gold-price?metal=both'))
          .timeout(const Duration(seconds: 15));
      if (response.statusCode == 200) {
        _data = json.decode(response.body);
        if (_data?['user_offset'] != null) {
          _userOffset = _data!['user_offset'] as int;
        }
        if (_data?['user_city'] != null) {
          _userCity = _data!['user_city'];
        }
        if (_data?['user_timezone'] != null) {
          _userTimezone = _data!['user_timezone'];
        }
        
        if (_data?['exchange_rates'] != null) {
          final er = _data!['exchange_rates'];
          final egp_rate = (er['official_usd_egp'] ?? 48.0) as num;
          _conversionRates['SAR'] = ((er['usd_sar'] ?? 3.75) as num).toDouble() / egp_rate.toDouble();
          _conversionRates['AED'] = ((er['usd_aed'] ?? 3.67) as num).toDouble() / egp_rate.toDouble();
        }
      } else {
         _errorMessage = "Server Error: ${response.statusCode}";
      }
      await fetchHistory();
    } catch (e) {
      debugPrint("Error fetching data: $e");
      if (e.toString().contains("SocketException") || e.toString().contains("HandshakeException")) {
        _errorMessage = _locale.languageCode == 'ar' ? "فشل الاتصال بالإنترنت" : "Internet Connection Failed";
      } else if (e.toString().contains("TimeoutException")) {
        _errorMessage = _locale.languageCode == 'ar' ? "انتهت مهلة الطلب، يرجى المحاولة مرة أخرى" : "Request timed out, please try again.";
      } else {
        _errorMessage = _locale.languageCode == 'ar' ? "حدث خطأ غير متوقع" : "An unexpected error occurred.";
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _startClock() {
    _clockTimer?.cancel();
    _clockTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      _currentTime = DateTime.now().toUtc().add(Duration(seconds: _userOffset));
      notifyListeners();
    });
  }

  void setCurrency(String cur) {
    _currentCurrency = cur;
    prefs.setString('currency', cur);
    notifyListeners();
  }

  @override
  void dispose() {
    _clockTimer?.cancel();
    super.dispose();
  }
}

class SaghaLiveApp extends StatelessWidget {
  const SaghaLiveApp({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<AppProvider>(context);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SaghaLive',
      locale: provider.locale,
      builder: (context, child) {
        return Directionality(
          textDirection: provider.locale.languageCode == 'ar' ? ui.TextDirection.rtl : ui.TextDirection.ltr,
          child: child!,
        );
      },
      theme: ThemeData(
        useMaterial3: true,
        brightness: provider.isDark ? Brightness.dark : Brightness.light,
        scaffoldBackgroundColor: provider.isDark ? AppColors.bgDark : AppColors.bgLight,
        colorSchemeSeed: AppColors.primary,
        textTheme: provider.locale.languageCode == 'ar' 
          ? GoogleFonts.cairoTextTheme(Theme.of(context).textTheme).apply(
              bodyColor: provider.isDark ? Colors.white : AppColors.textMainLight,
              displayColor: provider.isDark ? Colors.white : AppColors.textMainLight,
            )
          : GoogleFonts.outfitTextTheme(Theme.of(context).textTheme).apply(
              bodyColor: provider.isDark ? Colors.white : AppColors.textMainLight,
              displayColor: provider.isDark ? Colors.white : AppColors.textMainLight,
            ),
      ),
      home: const HomeScreen(),
    );
  }
}

// ... (HomeScreen same structure, updated build methods below)

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // ... (Timer init same) 
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<AppProvider>(context, listen: false).fetchData();
    });
    _timer = Timer.periodic(const Duration(seconds: 10), (timer) {
      Provider.of<AppProvider>(context, listen: false).fetchData();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _shareOnWhatsApp(AppProvider provider) async {
    final data = provider.data;
    if (data == null) return;

    final isAr = provider.locale.languageCode == 'ar';
    final now = DateTime.now();
    final dateStr = DateFormat('yyyy-MM-dd').format(now);
    final numFormat = NumberFormat("#,##0");

    // Get Current Company from Calculator State
    final selectedCompObj = _companies.firstWhere((c) => c['id'] == _calcCompanyId, orElse: () => _companies[0]);
    final compName = isAr ? (selectedCompObj['ar'] ?? selectedCompObj['id']) : (selectedCompObj['en'] ?? selectedCompObj['id']);
    
    final isGold = provider.activeMetal == 'gold';
    
    String text = isAr 
      ? "*بوابة المعادن المصرية* 🇪🇬\nتاريخ: $dateStr\n\n"
      : "*Egyptian Metal Portal* 🇪🇬\nDate: $dateStr\n\n";

    text += isAr ? "الشركة: $compName\n" : "Company: $compName\n";
    text += isAr ? "المعدن: ${isGold ? 'ذهب' : 'فضة'}\n" : "Metal: ${isGold ? 'Gold' : 'Silver'}\n";
    text += "------------------\n";

    if (isGold) {
      // 1. Gold Bars (24K)
      text += isAr ? "🏆 *سبائك الذهب (عيار ٢٤) - $compName:*\n" : "🏆 *Gold Bars (24K) - $compName:*\n";
      final price24g = (data['gold']['egp']['price'] as num).toDouble() / 31.1034768;
      
      final barWeights = [1.0, 2.5, 5.0, 10.0, 20.0, 31.1035, 50.0, 100.0];
      for (var w in barWeights) {
        final wObj = _allWeights.firstWhere((aw) => aw['val'] == w, orElse: () => {});
        if (wObj.isEmpty) continue;
        
        double price = price24g * w;
        // Apply Fees
        final fees = selectedCompObj['fees'] as Map<String, dynamic>? ?? {};
        final weightKey = w.toInt() == w ? w.toInt().toString() : w.toString();
        if (fees.containsKey(weightKey)) {
          price += (fees[weightKey] as num).toDouble() * w;
        }
        
        text += "${isAr ? wObj['text_ar'] : wObj['text_en']}: ${numFormat.format(price)} ${isAr ? 'ج.م' : 'EGP'}\n";
      }

      text += "\n";

      // 2. Gold Coins (21K)
      text += isAr ? "🪙 *عملات الذهب (عيار ٢١):*\n" : "🪙 *Gold Coins (21K):*\n";
      final price21g = (price24g * 21) / 24;
      final coinWeights = [8.0, 4.0, 2.0, 40.0];
      for (var w in coinWeights) {
        final wObj = _allWeights.firstWhere((aw) => aw['val'] == w, orElse: () => {});
        if (wObj.isEmpty) continue;

        double price = price21g * w;
        // Apply Fees
        final fees21 = selectedCompObj['fees_21k'] as Map<String, dynamic>? ?? {};
        final weightKey = w.toInt().toString();
        if (fees21.containsKey(weightKey)) {
          price += (fees21[weightKey] as num).toDouble() * w;
        } else if (selectedCompObj['id'] == 'btc') {
          price += 75.0 * w; // Default BTC fee for coins if not in map
        }
        
        text += "${isAr ? wObj['text_ar'] : wObj['text_en']}: ${numFormat.format(price)} ${isAr ? 'ج.م' : 'EGP'}\n";
      }
    } else {
      // Silver
      text += isAr ? "🥈 *سبائك الفضة (عيار ٩٩٩):*\n" : "🥈 *Silver Bars (999):*\n";
      final silverEgp = (data['silver']['egp']['price'] as num).toDouble();
      final price999g = silverEgp / 31.1;
      final silverWeights = [10.0, 20.0, 31.1035, 50.0, 100.0, 250.0, 500.0, 1000.0];
      
      for (var w in silverWeights) {
        final wObj = _allWeights.firstWhere((aw) => aw['val'] == w, orElse: () => {});
        if (wObj.isEmpty) continue;

        double price = price999g * w;
        // Apply Fees
        final feesS = selectedCompObj['fees_silver'] as Map<String, dynamic>? ?? {};
        final weightKey = w.toInt() == w ? w.toInt().toString() : w.toString();
        if (feesS.containsKey(weightKey)) {
          price += (feesS[weightKey] as num).toDouble() * w;
        }

        text += "${isAr ? wObj['text_ar'] : wObj['text_en']}: ${numFormat.format(price)} ${isAr ? 'ج.م' : 'EGP'}\n";
      }
    }

    text += isAr ? "\nتابع الأسعار لحظة بلحظة:\nhttps://saghalive.com" : "\nFollow live rates:\nhttps://saghalive.com";

    final url = "https://wa.me/?text=${Uri.encodeComponent(text)}";
    try {
      if (await canLaunchUrl(Uri.parse(url))) {
        await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
      }
    } catch (e) {
      debugPrint("WhatsApp Share Error: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<AppProvider>(context);
    // ... (rest of build)
    final isAr = provider.locale.languageCode == 'ar';
    final data = provider.data;

    return Scaffold(
      floatingActionButton: data != null ? FloatingActionButton(
        onPressed: () => _shareOnWhatsApp(provider),
        backgroundColor: const Color(0xFF25D366), // WhatsApp Green
        child: const Icon(FontAwesomeIcons.whatsapp, color: Colors.white, size: 30),
      ) : null,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 120),
          child: Column(
            children: [
              _buildHeader(context, provider),
              const SizedBox(height: 30),
              _buildTabs(context, provider),
              const SizedBox(height: 30),
              if (data != null) 
                _buildMainCard(context, provider, data)
              else if (provider.isLoading) 
                const Center(child: CircularProgressIndicator(color: AppColors.primary))
              else 
                Center(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      children: [
                        const Text("Connection Failed", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 10),
                         // Show actual error for debugging
                        Text(provider.errorMessage ?? "Unknown Error", 
                             textAlign: TextAlign.center,
                             style: const TextStyle(color: Colors.grey, fontSize: 12)),
                        const SizedBox(height: 20),
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary, foregroundColor: Colors.black),
                          onPressed: () => provider.fetchData(),
                          child: const Text("Retry"),
                        )
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 30),
              if (data != null) _buildGridPrices(context, provider, data),
              const SizedBox(height: 40),
              if (data != null) _buildCharts(context, provider),
              const SizedBox(height: 30),
              if (provider.analysisData != null) _buildAnalysis(context, provider),
              const SizedBox(height: 40),
              if (data != null) _buildBudgetPlanner(context, provider, data),
              const SizedBox(height: 40),
              if (data != null) _buildCalculator(context, provider, data),
              const SizedBox(height: 50),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildBudgetPlanner(BuildContext context, AppProvider provider, Map<String, dynamic> data) {
    final isAr = provider.locale.languageCode == 'ar';
    final isDark = provider.isDark;
    final curr = provider.currentCurrency;

    return Container(
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF0F172A).withOpacity(0.5) : Colors.white,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: AppColors.primary.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.account_balance_wallet, color: AppColors.primary),
              const SizedBox(width: 10),
              Text(
                isAr ? "مخطط الميزانية الذكي" : "SMART BUDGET PLANNER",
                style: GoogleFonts.outfit(fontSize: 18, fontWeight: FontWeight.bold, color: isDark ? Colors.white : Colors.black87),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Text(
             isAr ? "نصائح استثمارية تناسب ميزانيتك." : "Investment advice tailored to your wallet.",
             style: const TextStyle(color: AppColors.textDim, fontSize: 13),
          ),
          const SizedBox(height: 25),
          
          TextField(
            controller: _budgetController,
            keyboardType: TextInputType.number,
            style: TextStyle(color: isDark ? Colors.white : Colors.black87, fontSize: 18),
            decoration: InputDecoration(
              hintText: isAr ? "أدخل ميزانيتك ($curr)" : "Your Budget ($curr)",
              hintStyle: TextStyle(color: isDark ? Colors.white.withOpacity(0.2) : Colors.black.withOpacity(0.3)),
              filled: true,
              fillColor: isDark ? Colors.white.withOpacity(0.05) : Colors.black.withOpacity(0.05),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(15), borderSide: BorderSide.none),
              suffixIcon: IconButton(
                onPressed: () => _planMyInvestment(provider),
                icon: const Icon(Icons.auto_awesome, color: AppColors.primary),
              ),
            ),
          ),
          
          if (_showBudgetResults) ...[
            const SizedBox(height: 30),
            ..._budgetPlans.map((plan) => _buildPlanCard(plan, isAr, isDark, curr)),
          ]
        ],
      ),
    );
  }

  Widget _buildPlanCard(Map<String, dynamic> plan, bool isAr, bool isDark, String curr) {
    final textColor = isDark ? Colors.white : Colors.black87;
    final cardColor = isDark ? Colors.white.withOpacity(0.03) : Colors.black.withOpacity(0.03);
    final borderColor = isDark ? Colors.white.withOpacity(0.05) : Colors.black.withOpacity(0.05);

    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: cardColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: borderColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            isAr ? plan['title_ar'] : plan['title_en'],
            style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 16),
          ),
          const SizedBox(height: 15),
          ...(plan['basket'] as List).map((item) => Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Text("${item['qty']}x", style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
                    const SizedBox(width: 8),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(isAr ? item['name_ar'] : item['name_en'], style: TextStyle(color: textColor, fontSize: 14)),
                        Text(
                           isAr ? (item['metal'] == 'gold' ? 'ذهب' : 'فضة') : (item['metal'] as String).toUpperCase(),
                           style: const TextStyle(color: AppColors.textDim, fontSize: 10),
                        ),
                      ],
                    ),
                  ],
                ),
                Text(
                   "${NumberFormat("#,##0").format(item['qty'] * item['itemCost'])} $curr",
                   style: TextStyle(color: textColor, fontSize: 14),
                ),
              ],
            ),
          )).toList(),
          Divider(color: isDark ? Colors.white10 : Colors.black12, height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
               Text(isAr ? "الإجمالي" : "Total", style: const TextStyle(color: AppColors.textDim, fontSize: 12)),
               Text(
                 "${NumberFormat("#,##0").format(plan['total'])} $curr",
                 style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 20),
               ),
            ],
          ),
          const SizedBox(height: 5),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
               Text(isAr ? "المتبقي" : "Remaining", style: const TextStyle(color: AppColors.textDim, fontSize: 11)),
               Text(
                 "${NumberFormat("#,##0").format(plan['remaining'])} $curr",
                 style: const TextStyle(color: AppColors.textDim, fontSize: 11),
               ),
            ],
          ),
        ],
      ),
    );
  }

  // --- Widgets with Dynamic Colors ---

  Widget _buildCurrencySwitcher(BuildContext context, AppProvider provider) {
    final isDark = provider.isDark;
    
    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withOpacity(0.05) : Colors.black.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _currBtn(provider, 'EGP', '🇪🇬'),
          _currBtn(provider, 'SAR', '🇸🇦'),
          _currBtn(provider, 'AED', '🇦🇪'),
        ],
      ),
    );
  }

  Widget _currBtn(AppProvider provider, String code, String flag) {
    final active = provider.currentCurrency == code;
    return GestureDetector(
      onTap: () => _handleCurrencyChange(provider, code),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: active ? AppColors.primary : Colors.transparent,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(
          children: [
            Text(flag, style: const TextStyle(fontSize: 14)),
            const SizedBox(width: 4),
            Text(
              code,
              style: TextStyle(
                color: active ? Colors.black : AppColors.textDim,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, AppProvider provider) {
    final isAr = provider.locale.languageCode == 'ar';
    final isDark = provider.isDark;
    
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const PulseDot(),
                const SizedBox(width: 8),
                Text(
                  isAr ? "بيانات السوق الحية" : "LIVE MARKET INTEL",
                  style: GoogleFonts.outfit(
                    fontSize: 10,
                    letterSpacing: 2,
                    color: AppColors.textDim,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 5),
            Text(
              isAr ? "بوابة المعادن" : "SaghaLive",
              style: GoogleFonts.outfit(
                fontSize: 28,
                fontWeight: FontWeight.w900,
                color: AppColors.primary,
                letterSpacing: -1,
              ),
            ),
          ],
        ),
        Row(
          children: [
            IconButton(
              onPressed: () => _showInfoBottomSheet(context, isAr, isDark),
              icon: Icon(Icons.info_outline, color: isDark ? Colors.white : Colors.black87),
            ),
            IconButton(
              onPressed: () => provider.toggleTheme(),
              icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode, color: isDark ? Colors.white : Colors.black87),
            ),
            IconButton(
              onPressed: () => provider.setLocale(isAr ? 'en' : 'ar'),
              icon: Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  border: Border.all(color: isDark ? Colors.white24 : Colors.black12),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  isAr ? "EN" : "ع",
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ),
            ),
          ],
        )
      ],
    );
  }

  // --- Budget Planner State ---
  final TextEditingController _budgetController = TextEditingController();
  List<Map<String, dynamic>> _budgetPlans = [];
  bool _showBudgetResults = false;

  void _handleCurrencyChange(AppProvider provider, String newCode) {
    if (provider.currentCurrency == newCode) return;
    
    final oldCode = provider.currentCurrency;
    final rates = provider.conversionRates;
    final oldRate = rates[oldCode] ?? 1.0;
    final newRate = rates[newCode] ?? 1.0;

    // 1. Convert budget input value
    final inputStr = _budgetController.text.replaceAll(',', '');
    if (inputStr.isNotEmpty) {
      final val = double.tryParse(inputStr);
      if (val != null && val > 0) {
        final converted = (val / oldRate) * newRate;
        _budgetController.text = converted.round().toString();
      }
    }

    // 2. Set the new currency
    provider.setCurrency(newCode);

    // 3. Re-run budget planner if results were visible
    if (_showBudgetResults) {
      _planMyInvestment(provider);
    }
  }


  void _planMyInvestment(AppProvider provider) {
    final budgetStr = _budgetController.text;
    if (budgetStr.isEmpty) return;
    
    final budget = double.tryParse(budgetStr) ?? 0;
    if (budget <= 0) return;

    final data = provider.data;
    if (data == null) return;

    final rate = provider.conversionRates[provider.currentCurrency] ?? 1.0;
    final g24k = ((data['gold']['egp']['price'] as num).toDouble() / 31.1034768) * rate;
    final g21k = (g24k * 21) / 24;
    final s999 = ((data['silver']['egp']['price'] as num).toDouble() / 31.1) * rate;

    // Item Pool (Mirrored from JS)
    final pool = [
        {'name_en': '1 Kilogram', 'name_ar': '١ كيلو', 'metal': 'gold', 'weight': 1000.0, 'purity': 24, 'fees': 31.5},
        {'name_en': '500 Grams', 'name_ar': '٥٠٠ جرام', 'metal': 'gold', 'weight': 500.0, 'purity': 24, 'fees': 32.5},
        {'name_en': '250 Grams', 'name_ar': '٢٥٠ جرام', 'metal': 'gold', 'weight': 250.0, 'purity': 24, 'fees': 35.0},
        {'name_en': '100 Grams', 'name_ar': '١٠٠ جرام', 'metal': 'gold', 'weight': 100.0, 'purity': 24, 'fees': 75.0},
        {'name_en': '50 Grams', 'name_ar': '٥٠ جرام', 'metal': 'gold', 'weight': 50.0, 'purity': 24, 'fees': 77.0},
        {'name_en': '1 Ounce', 'name_ar': 'أونصة', 'metal': 'gold', 'weight': 31.1035, 'purity': 24, 'fees': 79.0},
        {'name_en': '20 Grams', 'name_ar': '٢٠ جرام', 'metal': 'gold', 'weight': 20.0, 'purity': 24, 'fees': 80.0},
        {'name_en': '10 Grams', 'name_ar': '١٠ جرام', 'metal': 'gold', 'weight': 10.0, 'purity': 24, 'fees': 82.0},
        {'name_en': '5 Grams', 'name_ar': '٥ جرام', 'metal': 'gold', 'weight': 5.0, 'purity': 24, 'fees': 85.0},
        {'name_en': '2.5 Grams', 'name_ar': '٢.٥ جرام', 'metal': 'gold', 'weight': 2.5, 'purity': 24, 'fees': 110.0},
        {'name_en': '1 Gram', 'name_ar': '١ جرام', 'metal': 'gold', 'weight': 1.0, 'purity': 24, 'fees': 185.0},
        {'name_en': '10 Coins', 'name_ar': '١٠ جنيهات', 'metal': 'gold', 'weight': 80.0, 'purity': 21, 'fees': 60.0},
        {'name_en': '5 Coins', 'name_ar': '٥ جنيهات', 'metal': 'gold', 'weight': 40.0, 'purity': 21, 'fees': 62.0},
        {'name_en': '1 Coin', 'name_ar': 'جنيه', 'metal': 'gold', 'weight': 8.0, 'purity': 21, 'fees': 75.0},
        {'name_en': 'Half Coin', 'name_ar': 'نصف جنيه', 'metal': 'gold', 'weight': 4.0, 'purity': 21, 'fees': 80.0},
        {'name_en': 'Quarter Coin', 'name_ar': 'ربع جنيه', 'metal': 'gold', 'weight': 2.0, 'purity': 21, 'fees': 85.0},
        {'name_en': '1 Kilogram', 'name_ar': '١ كيلو', 'metal': 'silver', 'weight': 1000.0, 'purity': 999, 'fees': 4.0},
        {'name_en': '500 Grams', 'name_ar': '٥٠٠ جرام', 'metal': 'silver', 'weight': 500.0, 'purity': 999, 'fees': 4.55},
        {'name_en': '250 Grams', 'name_ar': '٢٥٠ جرام', 'metal': 'silver', 'weight': 250.0, 'purity': 999, 'fees': 4.85},
        {'name_en': '100 Grams', 'name_ar': '١٠٠ جرام', 'metal': 'silver', 'weight': 100.0, 'purity': 999, 'fees': 12.0},
        {'name_en': '50 Grams', 'name_ar': '٥٠ جرام', 'metal': 'silver', 'weight': 50.0, 'purity': 999, 'fees': 13.0},
        {'name_en': '1 Ounce', 'name_ar': 'أونصة', 'metal': 'silver', 'weight': 31.1035, 'purity': 999, 'fees': 14.0},
        {'name_en': '10 Grams', 'name_ar': '١٠ جرام', 'metal': 'silver', 'weight': 10.0, 'purity': 999, 'fees': 16.0},
    ];

    Map<String, dynamic> calculateBasket(double targetBudget, bool Function(Map<String, dynamic>) filter) {
      double rem = targetBudget;
      List<Map<String, dynamic>> basket = [];
      double total = 0;
      
      final filtered = pool.where(filter).toList();
      filtered.sort((a, b) => (b['weight'] as double).compareTo(a['weight'] as double));

      for (var item in filtered) {
        double base = item['metal'] == 'gold' 
          ? (item['purity'] == 24 ? g24k : g21k)
          : s999;
        double costPerItem = (base + ((item['fees'] as double) * rate)) * (item['weight'] as double);
        
        if (rem >= costPerItem) {
          int qty = (rem / costPerItem).floor();
          basket.add({
            'name_en': item['name_en'],
            'name_ar': item['name_ar'],
            'metal': item['metal'],
            'qty': qty,
            'itemCost': costPerItem
          });
          rem -= qty * costPerItem;
          total += qty * costPerItem;
        }
      }
      return {'basket': basket, 'total': total, 'remaining': rem};
    }

    final goldPlan = calculateBasket(budget, (i) => i['metal'] == 'gold');
    final silverPlan = calculateBasket(budget, (i) => i['metal'] == 'silver');
    
    // Mixed Logic
    final mixedGold = calculateBasket(budget * 0.9, (i) => i['metal'] == 'gold');
    final mixedSilver = calculateBasket((budget * 0.1) + (mixedGold['remaining'] as double), (i) => i['metal'] == 'silver');
    
    final mixedPlan = {
      'basket': [...(mixedGold['basket'] as List), ...(mixedSilver['basket'] as List)],
      'total': (mixedGold['total'] as double) + (mixedSilver['total'] as double),
      'remaining': mixedSilver['remaining']
    };

    setState(() {
      _budgetPlans = [
        {'id': 'gold', 'title_en': 'Gold Investment Plan', 'title_ar': 'خطة استثمار الذهب', ...goldPlan},
        {'id': 'silver', 'title_en': 'Silver Growth Plan', 'title_ar': 'خطة استثمار الفضة', ...silverPlan},
        {'id': 'mixed', 'title_en': 'Diversified Plan (90% Gold)', 'title_ar': 'خطة التنويع (٩٠٪ ذهب)', ...mixedPlan},
      ].where((p) => (p['basket'] as List).isNotEmpty).toList();
      _showBudgetResults = true;
    });
  }

  Widget _buildMainCard(BuildContext context, AppProvider provider, Map<String, dynamic> data) {
    final isGold = provider.activeMetal == 'gold';
    final isDark = provider.isDark;
    final metalData = isGold ? data['gold'] : data['silver'];
    double price = (metalData['egp']['price'] ?? 0).toDouble();
    final usdPrice = (metalData['usd']['price'] ?? 0).toDouble();
    final priceFmt = NumberFormat("#,##0.00", "en_US").format(price);
    final usdFmt = NumberFormat("#,##0.00", "en_US").format(usdPrice);
    final textColor = isDark ? Colors.white : AppColors.textMainLight;

    double prevPrice = (metalData['egp']['prev_close_price'] ?? price).toDouble();
    final diff = price - prevPrice;
    final percent = prevPrice != 0 ? (diff / prevPrice) * 100 : 0.0;
    final isUp = diff >= 0;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 20),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF111111) : Colors.white,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: isDark ? Colors.white10 : Colors.black12),
        boxShadow: [
           BoxShadow(color: Colors.black.withOpacity(isDark ? 0.5 : 0.05), blurRadius: 30, offset: const Offset(0, 10))
        ]
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                provider.locale.languageCode == 'ar' 
                  ? (isGold ? "سعر الذهب الحالي" : "سعر الفضة الحالي")
                  : (isGold ? "CURRENT GOLD PRICE" : "CURRENT SILVER PRICE"),
                style: GoogleFonts.outfit(color: AppColors.textDim, letterSpacing: 2, fontSize: 10),
              ),
              _buildCurrencySwitcher(context, provider),
            ],
          ),
          const SizedBox(height: 25),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                NumberFormat("#,##0.00").format(price * provider.conversionRates[provider.currentCurrency]!),
                style: GoogleFonts.outfit(
                  fontSize: 52, fontWeight: FontWeight.w900,
                  color: textColor, letterSpacing: -3,
                ),
              ),
              const SizedBox(width: 8),
              Text(
                provider.currentCurrency, 
                style: GoogleFonts.outfit(
                  fontSize: 16, 
                  color: isGold ? AppColors.primary : AppColors.silver, 
                  fontWeight: FontWeight.bold
                )
              ),
            ],
          ),
          const SizedBox(height: 10),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("$usdFmt USD / OZ", style: GoogleFonts.outfit(color: AppColors.textDim, fontSize: 14)),
              const SizedBox(width: 15),
              // Daily Change Badge
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: (isUp ? Colors.green : Colors.red).withOpacity(0.15),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: (isUp ? Colors.green : Colors.red).withOpacity(0.3)),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      isUp ? Icons.arrow_drop_up : Icons.arrow_drop_down,
                      color: isUp ? Colors.green : Colors.red,
                      size: 20,
                    ),
                    Text(
                      "${isUp ? '+' : '-'}${percent.abs().toStringAsFixed(2)}%",
                      style: TextStyle(
                        color: isUp ? Colors.green : Colors.red,
                        fontWeight: FontWeight.bold,
                        fontSize: 13,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _showInfoBottomSheet(BuildContext context, bool isAr, bool isDark) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => Container(
        height: MediaQuery.of(context).size.height * 0.9,
        decoration: const BoxDecoration(
          color: Color(0xFF111111),
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Stack(
          children: [
            Positioned(
              right: 20, top: 20,
              child: IconButton(
                icon: const Icon(Icons.close, color: Colors.white, size: 28),
                onPressed: () => Navigator.pop(context),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                     Container(
                     width: 100, height: 100,
                     padding: EdgeInsets.zero, // Removed padding
                     decoration: BoxDecoration(
                        color: Colors.black,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: Colors.white10)
                     ),
                     child: Padding(
                       padding: const EdgeInsets.all(8.0),
                       child: Image.asset('assets/icon.png', fit: BoxFit.contain),
                     ),
                   ),
                   const SizedBox(height: 20),
                   Text("SaghaLive", style: GoogleFonts.outfit(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white)),
                   const SizedBox(height: 5),
                   Text("Version 1.0.0", style: GoogleFonts.outfit(fontSize: 14, color: Colors.grey)),
                   const SizedBox(height: 30),
                   Text("Egyptian Gold & Currency Prices", style: GoogleFonts.outfit(fontSize: 18, color: Colors.white)),
                   const SizedBox(height: 50),
                   Text("Developed by", style: GoogleFonts.outfit(fontSize: 14, color: Colors.grey)),
                   const SizedBox(height: 5),
                   Text("Tamer Elwakeel", style: GoogleFonts.outfit(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                   const SizedBox(height: 5),
                   MouseRegion(cursor: SystemMouseCursors.click, child: GestureDetector(
                       onTap: () async {
                           try { await launchUrl(Uri.parse('https://saghalive.com')); } catch (_) {}
                       },
                       child: Text("saghalive.com", style: GoogleFonts.outfit(fontSize: 14, color: AppColors.primary))
                   )),

                   const SizedBox(height: 50),

                   MouseRegion(cursor: SystemMouseCursors.click, child: GestureDetector(
                       onTap: () {
                           Navigator.pop(context); // Close Bottom Sheet First
                           Navigator.push(context, MaterialPageRoute(builder: (_) => const ContactUsPage()));
                       },
                       child: Text(isAr ? "تواصل معنا" : "Contact Us", style: GoogleFonts.outfit(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white))
                   )),

                   const SizedBox(height: 40),
                   Row(
                     mainAxisAlignment: MainAxisAlignment.center,
                     children: [
                        TextButton(
                           onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PrivacyPolicyPage())),
                           child: Text("Privacy Policy", style: GoogleFonts.outfit(color: Colors.white, decoration: TextDecoration.underline))
                        ),
                        const Text("|", style: TextStyle(color: Colors.grey)),
                        TextButton(
                           onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const TermsOfUsePage())),
                           child: Text("Terms of Use", style: GoogleFonts.outfit(color: Colors.white, decoration: TextDecoration.underline))
                        ),
                     ],
                   ),
                   const SizedBox(height: 10),
                   Text("Copyright © 2026 - All rights reserved", style: GoogleFonts.outfit(fontSize: 12, color: Colors.grey[700])),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  // --- Calculator State ---
  String _calcPurity = '24';
  String _calcCompanyId = 'btc';
  dynamic _calcWeight = 10;
  
  // Companies Data (Mirrored from Web)
  final List<Map<String, dynamic>> _companies = [
    {
      'id': 'btc', 'en': 'BTC', 'ar': 'BTC',
      'fees': { '1': 185, '2.5': 110, '5': 85, '10': 82, '20': 80, '31.1035': 79, '50': 77, '100': 75, '116.64': 65, '250': 35, '500': 32.5, '1000': 31.5 },
      'allowed_weights': ['1', '2.5', '5', '10', '20', '31.1035', '50', '100', '116.64', '250', '500', '1000'],
      'fees_21k': {'2': 85, '4': 80, '8': 75, '40': 62, '80': 60},
      'allowed_weights_21k': ['2', '4', '8', '40', '80'],
      'fees_silver': {'5': 19.5, '10': 16, '20': 15, '31.1035': 14, '50': 13, '100': 12, '116.64': 10.5, '250': 4.85, '500': 4.55, '1000': 4, '5000': 3.9},
      'allowed_weights_silver': ['5', '10', '20', '31.1035', '50', '100', '116.64', '250', '500', '1000', '5000']
    },
    {
      'id': 'elgalla', 'en': 'ElGalla Gold', 'ar': 'ElGalla Gold',
      'fees': { '1': 150, '2.5': 100, '2.5_bb': 120, '5': 77, '5_bb': 110, '10': 75, '15.55': 75, '20': 74, '31.1035': 73, '50': 71, '100': 70, '116.64': 60, '250': 48, '500': 47, '1000': 45 },
      'allowed_weights': ['1', '2.5', '2.5_bb', '5', '5_bb', '10', '15.55', '20', '31.1035', '50', '100', '116.64', '250', '500', '1000'],
      'fees_21k': {'2': 90, '4': 75, '8': 70, '40': 60},
      'allowed_weights_21k': ['2', '4', '8', '40']
    },
    {
      'id': 'gfg', 'en': 'GFG', 'ar': 'GFG',
      'fees': { '0.5': 100, '1': 80, '2.5': 70, '10': 52, '31.1035': 48, '50': 38, '100': 38 },
      'allowed_weights': ['0.5', '1', '2.5', '10', '31.1035', '50', '100'],
      'fees_21k': {'2': 53, '4': 50, '8': 48},
      'allowed_weights_21k': ['2', '4', '8']
    },
    {
      'id': 'gold_era', 'en': 'Gold ERA', 'ar': 'Gold ERA',
      'fees': { '0.25': 724, '0.5': 342, '1': 161, '2.5': 96, '5': 66, '10': 65, '15.55': 64, '20': 64, '31.1035': 63, '50': 61, '100': 59, '116.64': 47, '250': 28.2, '500': 28.1, '1000': 26.05 },
      'allowed_weights': ['0.25', '0.5', '1', '2.5', '5', '10', '15.55', '20', '31.1035', '50', '100', '250', '500', '1000'],
      'fees_21k': {'2': 63, '4': 60, '8': 55},
      'allowed_weights_21k': ['2', '4', '8']
    },
    {
      'id': 'mb_gold', 'en': 'MB Gold', 'ar': 'MB Gold',
      'fees': { '1': 175, '2.5': 100, '5': 67, '10': 66, '20': 64, '31.1035': 62, '50': 60, '100': 59, '116.64': 47.5, '250': 30.7 },
      'allowed_weights': ['1', '2.5', '5', '10', '20', '31.1035', '50', '100', '116.64', '250'],
      'fees_21k': {'2': 66, '4': 60, '8': 54, '40': 53},
      'allowed_weights_21k': ['2', '4', '8', '40']
    },
    {
      'id': 'sam', 'en': 'SAM', 'ar': 'SAM',
      'fees': { '1': 135, '2.5': 66, '5': 60, '10': 60, '15.55': 56, '20': 56, '31.1035': 56, '50': 55.5, '100': 55, '116.64': 41.5 },
      'allowed_weights': ['1', '2.5', '5', '10', '15.55', '20', '31.1035', '50', '100', '116.64'],
      'fees_21k': {'2': 53.5, '4': 50.5, '8': 48.5},
      'allowed_weights_21k': ['2', '4', '8'],
      'fees_silver': {'2.5': 25, '5': 23, '10': 20, '20': 18, '31.1035': 15, '31.1035_r': 15, '100': 13, '250': 4.2, '500': 4, '1000': 3},
      'allowed_weights_silver': ['2.5', '5', '10', '20', '31.1035', '31.1035_r', '100', '250', '500', '1000']
    },
    {
      'id': 'selema', 'en': 'Selema', 'ar': 'Selema',
      'fees': { '1': 120, '5': 58, '10': 57, '20': 55, '31.1035': 53, '50': 51, '100': 48, '250': 30, '500': 28, '1000': 26 },
      'allowed_weights': ['1', '5', '10', '20', '31.1035', '50', '100', '250', '500', '1000'],
      'fees_21k': {'2': 57, '4': 57, '8': 47, '40': 42, '50': 41, '100': 41, '250': 28, '500': 26, '1000': 24},
      'allowed_weights_21k': ['2', '4', '8', '40', '50', '100', '250', '500', '1000']
    },
    {
      'id': 'swiss_gold', 'en': 'Swiss Gold', 'ar': 'Swiss Gold',
      'fees': { '1': 165, '5': 65, '10': 65, '20': 53, '31.1035': 53, '50': 52, '100': 52 },
      'allowed_weights': ['1', '5', '10', '20', '31.1035', '50', '100'],
      'fees_21k': {'2': 100, '4': 75, '8': 45},
      'allowed_weights_21k': ['2', '4', '8']
    },
    {
      'id': 'al_rai', 'en': 'Al-Ra\'i', 'ar': 'الراعي',
      'fees': { '0.25': 600, '0.5': 300, '1': 130, '2.5': 60, '5': 55, '10': 55, '20': 55, '31.1035': 50, '50': 50, '100': 35, '250': 16, '500': 15, '1000': 14 },
      'allowed_weights': ['0.25', '0.5', '1', '2.5', '5', '10', '20', '31.1035', '50', '100', '250', '500', '1000'],
      'fees_21k': {'2': 55, '4': 50, '8': 45},
      'allowed_weights_21k': ['2', '4', '8'],
      'fees_silver': {'1000': 4},
      'allowed_weights_silver': ['1000']
    },
    {
      'id': 'najm_al_din', 'en': 'Najm Al-Din', 'ar': 'نجم الدين',
      'fees': { '0.25': 400, '0.5': 180, '1': 80, '2.5': 70, '5': 60, '10': 60, '20': 60, '31.1035': 60, '50': 60, '100': 60, '250': 40, '500': 30, '1000': 25, '5000': 17 },
      'allowed_weights': ['0.25', '0.5', '1', '2.5', '5', '10', '20', '31.1035', '50', '100', '250', '500', '1000', '5000'],
      'fees_21k': {'2': 55, '4': 50, '8': 45},
      'allowed_weights_21k': ['2', '4', '8'],
      'fees_silver': {'8': 18, '10': 18, '20': 16, '31.1035': 16, '50': 14, '100': 12, '250': 10, '500': 8, '1000': 6, '5000': 2, '15000': 3},
      'allowed_weights_silver': ['8', '10', '20', '31.1035', '50', '100', '250', '500', '1000', '5000', '15000']
    }
  ];

  // Standard Weights for Dropdown
  final List<Map<String, dynamic>> _allWeights = [
    { 'val': 0.25, 'weight': 0.25, 'text_en': "1/4 Gram", 'text_ar': "ربع جرام" },
    { 'val': 0.5, 'weight': 0.5, 'text_en': "1/2 Gram", 'text_ar': "نصف جرام" },
    { 'val': 1.0, 'weight': 1.0, 'text_en': "1 Gram", 'text_ar': "١ جرام" },
    { 'val': 2.0, 'weight': 2.0, 'text_en': "Quarter Coin", 'text_ar': "ربع جنيه" },
    { 'val': 2.5, 'weight': 2.5, 'text_en': "2.5 Grams", 'text_ar': "٢.٥ جرام" },
    { 'val': '2.5_bb', 'weight': 2.5, 'text_en': "2.5g (Bubble)", 'text_ar': "٢.٥ جرام (بابل)" },
    { 'val': 4.0, 'weight': 4.0, 'text_en': "Half Coin", 'text_ar': "نصف جنيه" },
    { 'val': 5.0, 'weight': 5.0, 'text_en': "5 Grams", 'text_ar': "٥ جرام" },
    { 'val': '5_bb', 'weight': 5.0, 'text_en': "5g (Bubble)", 'text_ar': "٥ جرام (بابل)" },
    { 'val': 8.0, 'weight': 8.0, 'text_en': "1 Coin", 'text_ar': "جنيه" },
    { 'val': 10.0, 'weight': 10.0, 'text_en': "10 Grams", 'text_ar': "١٠ جرام" },
    { 'val': 15.55, 'weight': 15.55, 'text_en': "Half Ounce", 'text_ar': "نصف أونصة" },
    { 'val': 20.0, 'weight': 20.0, 'text_en': "20 Grams", 'text_ar': "٢٠ جرام" },
    { 'val': 31.1035, 'weight': 31.1035, 'text_en': "1 Ounce", 'text_ar': "أونصة" },
    { 'val': '31.1035_r', 'weight': 31.1035, 'text_en': "Round Ounce", 'text_ar': "أونصة دائرية" },
    { 'val': 40.0, 'weight': 40.0, 'text_en': "5 Coins", 'text_ar': "٥ جنيهات" },
    { 'val': 50.0, 'weight': 50.0, 'text_en': "50 Grams", 'text_ar': "٥٠ جرام" },
    { 'val': 80.0, 'weight': 80.0, 'text_en': "10 Coins", 'text_ar': "١٠ جنيهات" },
    { 'val': 100.0, 'weight': 100.0, 'text_en': "100 Grams", 'text_ar': "١٠٠ جرام" },
    { 'val': 116.64, 'weight': 116.64, 'text_en': "10 Tola", 'text_ar': "١٠ تولا" },
    { 'val': 250.0, 'weight': 250.0, 'text_en': "250 Grams", 'text_ar': "٢٥٠ جرام" },
    { 'val': 500.0, 'weight': 500.0, 'text_en': "500 Grams", 'text_ar': "٥٠٠ جرام" },
    { 'val': 1000.0, 'weight': 1000.0, 'text_en': "1 Kilogram", 'text_ar': "١ كيلو" },
    { 'val': 5000.0, 'weight': 5000.0, 'text_en': "5 Kg", 'text_ar': "٥ كيلو" },
    { 'val': 15000.0, 'weight': 15000.0, 'text_en': "15 Kg", 'text_ar': "١٥ كيلو" },
  ];

  Widget _buildCalculator(BuildContext context, AppProvider provider, Map<String, dynamic> data) {
    final isAr = provider.locale.languageCode == 'ar';
    final isGold = provider.activeMetal == 'gold';

    // Filter Companies for Silver (Only those with silver fees)
    final availableCompanies = isGold 
      ? _companies 
      : _companies.where((c) => c.containsKey('fees_silver')).toList();

    // Ensure _calcCompanyId is valid
    if (!availableCompanies.any((c) => c['id'] == _calcCompanyId)) {
        _calcCompanyId = availableCompanies[0]['id'];
    }
    
    // 1. Determine Filtering Logic
    List<Map<String, dynamic>> filteredWeights = _allWeights;
    final selectedCompObj = _companies.firstWhere((c) => c['id'] == _calcCompanyId, orElse: () => _companies[0]);
    
    List<String>? allowed;
    if (isGold) {
        if (_calcPurity == '21' && selectedCompObj['allowed_weights_21k'] != null) {
            allowed = (selectedCompObj['allowed_weights_21k'] as List).map((e) => e.toString()).toList();
        } else if (selectedCompObj['allowed_weights'] != null) {
            allowed = (selectedCompObj['allowed_weights'] as List).map((e) => e.toString()).toList();
        }
    } else {
        // Silver Logic
        if (selectedCompObj['allowed_weights_silver'] != null) {
             allowed = (selectedCompObj['allowed_weights_silver'] as List).map((e) => e.toString()).toList();
        } else {
             // Default Silver Weights
             allowed = ['5', '10', '20', '31.1035', '50', '100', '116.64', '250', '500', '1000', '5000'];
        }
    }

    if (allowed != null) {
         filteredWeights = _allWeights.where((w) {
             final val = w['val'];
             // Ensure it's in allowed list
             return allowed!.contains(val.toString()) || 
                    (val is num && allowed!.contains(val.toInt().toString()));
         }).toList();
    }
    
    // 2. Validate Selection
    bool isValid = filteredWeights.any((w) => w['val'].toString() == _calcWeight.toString());
    if (!isValid) {
       if (filteredWeights.isNotEmpty) _calcWeight = filteredWeights[0]['val'];
    }

    // 3. Price Logic
    double unitPrice = 0;
    if (isGold) {
      double price24 = (data['gold']['egp']['price'] as num).toDouble() / 31.1034768;
      if (_calcPurity == '24') unitPrice = price24;
      else if (_calcPurity == '21') unitPrice = (price24 * 21) / 24;
      else if (_calcPurity == '18') unitPrice = (price24 * 18) / 24;
    } else {
       final silverEgp = (data['silver']['egp']['price'] as num).toDouble();
       unitPrice = silverEgp / 31.1; 
    }

    // 4. Fee Logic
    double feesPerGram = 0;
    Map<String, dynamic> feesMap = {};
    
    if (isGold) {
        if (_calcPurity == '21' && selectedCompObj['fees_21k'] != null) {
            feesMap = selectedCompObj['fees_21k'];
        } else {
            feesMap = selectedCompObj['fees'] ?? {};
        }
    } else {
        if (selectedCompObj['fees_silver'] != null) {
            feesMap = selectedCompObj['fees_silver'];
        }
    }

    String weightKey = _calcWeight.toString(); 
    if (_calcWeight is num) {
         // Try integer key first if it's integer (e.g. 1.0 -> "1")
         if (_calcWeight == _calcWeight.toInt()) {
             if (feesMap.containsKey(_calcWeight.toInt().toString())) {
                  weightKey = _calcWeight.toInt().toString();
             }
         }
    }
    
    if (feesMap.containsKey(weightKey)) {
        feesPerGram = (feesMap[weightKey] as num).toDouble();
    } else if (weightKey.endsWith(".0") && feesMap.containsKey(weightKey.replaceAll(".0", ""))) {
         feesPerGram = (feesMap[weightKey.replaceAll(".0", "")] as num).toDouble();
    }

    // 5. Total
    double weightVal = 0;
    if (_calcWeight is num) {
        weightVal = (_calcWeight as num).toDouble();
    } else {
        final wObj = _allWeights.firstWhere((w) => w['val'].toString() == _calcWeight.toString(), orElse: () => {'weight': 0.0});
        weightVal = (wObj['weight'] as num).toDouble();
    }

    double totalFees = feesPerGram * weightVal;
    double totalGoldPrice = unitPrice * weightVal;
    double grandTotal = totalGoldPrice + totalFees;

    final isDark = provider.isDark;
    final textColor = isDark ? Colors.white : Colors.black87;
    final inputBg = isDark ? Colors.white.withOpacity(0.05) : Colors.black.withOpacity(0.05);

    return Container(
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: isDark ? AppColors.cardBg : Colors.white,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: isDark ? Colors.white10 : Colors.black12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.calculate, color: AppColors.primary),
              const SizedBox(width: 10),
              Text(
                isAr ? "حاسبة الاستثمار" : "INVESTMENT CALCULATOR",
                style: GoogleFonts.outfit(
                  fontSize: 18, fontWeight: FontWeight.bold, color: textColor
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          // Company Selector (Visible for Silver now too if configured)
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(isAr ? "الشركة" : "Company", style: GoogleFonts.outfit(color: AppColors.textDim)),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 15),
                decoration: BoxDecoration(color: inputBg, borderRadius: BorderRadius.circular(12)),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: _calcCompanyId,
                    isExpanded: true,
                    dropdownColor: isDark ? Colors.grey[900] : Colors.white,
                    items: availableCompanies.map((c) => DropdownMenuItem(
                      value: c['id'] as String,
                      child: Text(isAr ? c['ar'] : c['en'], style: TextStyle(color: textColor)),
                    )).toList(),
                    onChanged: (val) => setState(() => _calcCompanyId = val!),
                  ),
                ),
              ),
              const SizedBox(height: 15),
            ],
          ),

          // Weight Selector
          Text(isAr ? "الوزن" : "Weight", style: GoogleFonts.outfit(color: AppColors.textDim)),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 15),
            decoration: BoxDecoration(color: inputBg, borderRadius: BorderRadius.circular(12)),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<dynamic>(
                value: _calcWeight,
                isExpanded: true,
                dropdownColor: isDark ? Colors.grey[900] : Colors.white,
                items: filteredWeights.map((w) => DropdownMenuItem(
                  value: w['val'],
                  child: Text(isAr ? w['text_ar'] : w['text_en'], style: TextStyle(color: textColor)),
                )).toList(),
                onChanged: (val) => setState(() => _calcWeight = val!),
              ),

            ),
          ),

          const SizedBox(height: 25),
          Divider(color: isDark ? Colors.white10 : Colors.black12),
          const SizedBox(height: 15),

          // Results
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(isAr ? "المصنعية" : "Making Fees", style: const TextStyle(color: AppColors.textDim)),
              Text("${NumberFormat("#,##0").format(totalFees)} EGP", style: TextStyle(color: textColor, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 10),
          Text(isAr ? "القيمة الإجمالية" : "Estimated Value", style: GoogleFonts.outfit(color: AppColors.textDim, letterSpacing: 1)),
          const SizedBox(height: 5),
          Text(
            "${NumberFormat("#,##0").format(grandTotal)} EGP",
            style: GoogleFonts.outfit(fontSize: 36, fontWeight: FontWeight.w900, color: AppColors.primary, letterSpacing: -1),
          ),
        ],
      ),
    );
  }



  Widget _buildCharts(BuildContext context, AppProvider provider) {
    final isAr = provider.locale.languageCode == 'ar';
    final isGold = provider.activeMetal == 'gold';
    final isDark = provider.isDark;
    final color = isGold ? AppColors.primary : AppColors.silver;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? AppColors.cardBg : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: isDark ? Colors.white10 : Colors.black12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                isAr ? "اتجاهات السوق" : "Market Trends",
                style: GoogleFonts.outfit(
                  fontSize: 18, fontWeight: FontWeight.bold,
                  color: isDark ? Colors.white : Colors.black87
                ),
              ),
              // Range Selector
              Row(
                children: ['24h', '1m', '1y'].map((range) {
                  final active = provider.chartRange == range;
                  return GestureDetector(
                    onTap: () => provider.setChartRange(range),
                    child: Container(
                      margin: const EdgeInsets.only(left: 8),
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(
                        color: active ? color : Colors.transparent,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: active ? color : (isDark ? Colors.white24 : Colors.black12)),
                      ),
                      child: Text(
                        range.toUpperCase(),
                        style: TextStyle(
                          fontSize: 10,
                          color: active ? (isDark ? Colors.black : Colors.white) : (isDark ? Colors.white : Colors.black54),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  );
                }).toList(),
              ),
            ],
          ),
          const SizedBox(height: 30),
          SizedBox(
            key: ValueKey("${provider.activeMetal}_${provider.chartRange}"), // Force Rebuild
            height: 200,
            child: provider.chartData.isEmpty
                ? Center(child: CircularProgressIndicator(color: isDark ? Colors.white24 : Colors.black12))
                : LineChart(
                    LineChartData(
                      gridData: FlGridData(
                        show: true,
                        getDrawingHorizontalLine: (value) => FlLine(color: isDark ? Colors.white10 : Colors.black.withOpacity(0.05), strokeWidth: 1),
                      ),
                      titlesData: FlTitlesData(
                        show: true,
                        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 45,
                            getTitlesWidget: (value, meta) {
                              if (value == meta.min || value == meta.max) return const SizedBox();
                              return Text(
                                NumberFormat.compact().format(value),
                                style: const TextStyle(color: AppColors.textDim, fontSize: 10),
                              );
                            },
                          ),
                        ),
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            interval: (provider.chartData.length / 4).clamp(1, 100).toDouble(),
                            getTitlesWidget: (value, meta) {
                              int index = value.toInt();
                              if (index >= 0 && index < provider.chartLabels.length) {
                                return Padding(
                                  padding: const EdgeInsets.only(top: 8.0),
                                  child: Text(
                                    provider.chartLabels[index],
                                    style: const TextStyle(color: AppColors.textDim, fontSize: 9),
                                  ),
                                );
                              }
                              return const SizedBox();
                            },
                          ),
                        ),
                      ),
                      borderData: FlBorderData(show: false),
                      lineTouchData: LineTouchData(
                         enabled: true,
                         touchTooltipData: LineTouchTooltipData(
                            tooltipBgColor: Colors.black.withOpacity(0.8),
                            getTooltipItems: (spots) => spots.map((s) => LineTooltipItem(
                               "${NumberFormat("#,##0").format(s.y)} EGP",
                               const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)
                            )).toList()
                         )
                      ),
                      minY: provider.chartData.map((e) => e.y).reduce(math.min) * 0.999,
                      maxY: provider.chartData.map((e) => e.y).reduce(math.max) * 1.001,
                      lineBarsData: [
                        LineChartBarData(
                          spots: provider.chartData,
                          isCurved: true,
                          color: color,
                          barWidth: 2,
                          dotData: const FlDotData(show: false),
                          belowBarData: BarAreaData(
                            show: true,
                            color: color.withOpacity(0.1),
                          ),
                        ),
                      ],
                    ),
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildAnalysis(BuildContext context, AppProvider provider) {
    if (provider.analysisData == null) return const SizedBox.shrink();
    
    final isAr = provider.locale.languageCode == 'ar';
    final isDark = provider.isDark;
    final data = provider.analysisData!;
    final score = data['score'] as int? ?? 50;
    
    Color scoreColor = AppColors.primary;
    if (score >= 60) scoreColor = AppColors.success;
    else if (score <= 40) scoreColor = AppColors.error;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? AppColors.cardBg : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: isDark ? Colors.white10 : Colors.black12),
      ),
      child: Column(
        children: [
          Row(
            children: [
              // Use Icon instead of FontAwesome for simplicity if not set up, or standard icon
              const Icon(Icons.psychology, color: AppColors.primary, size: 24),
              const SizedBox(width: 10),
              Text(
                isAr ? "تحليل السوق الذكي" : "Smart Market Analysis",
                style: GoogleFonts.outfit(
                  fontSize: 18, fontWeight: FontWeight.bold,
                  color: isDark ? Colors.white : Colors.black87
                ),
              ),
            ],
          ),
          const SizedBox(height: 30),
          // Gauge / Score
          Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                width: 160, height: 160,
                child: CircularProgressIndicator(
                  value: score / 100,
                  strokeWidth: 12,
                  backgroundColor: isDark ? Colors.white10 : Colors.black12,
                  color: scoreColor,
                ),
              ),
              Column(
                children: [
                  Text(
                    "$score",
                    style: GoogleFonts.outfit(
                      fontSize: 56, fontWeight: FontWeight.w900, 
                      color: isDark ? Colors.white : Colors.black87
                    ),
                  ),
                  Text(
                    () {
                      String rec = data['recommendation'] ?? 'NEUTRAL';
                      if (!isAr) return rec;
                      switch(rec.toUpperCase()) {
                        case 'STRONG BUY': return "شراء قوي";
                        case 'BUY': return "شراء";
                        case 'SELL': return "بيع";
                        case 'STRONG SELL': return "بيع قوي";
                        case 'NEUTRAL': return "محايد";
                        default: return rec;
                      }
                    }(),
                    style: GoogleFonts.outfit(
                      color: scoreColor, fontWeight: FontWeight.bold, fontSize: 16
                    ),
                  ),
                ],
              )
            ],
          ),
          const SizedBox(height: 30),
          // Indicators Grid
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildIndicatorItem("RSI", "${data['rsi'] ?? '--'}", isAr, isDark),
              Container(width: 1, height: 40, color: isDark ? Colors.white10 : Colors.black12),
              _buildIndicatorItem("Trend", "${data['trend'] ?? '--'}", isAr, isDark),
              Container(width: 1, height: 40, color: isDark ? Colors.white10 : Colors.black12),
              _buildIndicatorItem("BB Status", "${data['bb_status'] ?? '--'}", isAr, isDark),
            ],
          ),
          const SizedBox(height: 25),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(15),
            decoration: BoxDecoration(
              color: isDark ? Colors.white.withOpacity(0.05) : Colors.black.withOpacity(0.05),
              borderRadius: BorderRadius.circular(15)
            ),
            child: Text(
               isAr 
                ? "تحليل فني للسوق بناءً على الزخم والاتجاه والتقلبات." 
                : "AI-powered technical analysis based on Momentum, Trend & Volatility.",
               textAlign: TextAlign.center,
               style: const TextStyle(color: AppColors.textDim, fontSize: 12),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildIndicatorItem(String label, String value, bool isAr, bool isDark) {
    String displayLabel = label;
    if (isAr) {
      if (label == "RSI") displayLabel = "القوة النسبية";
      if (label == "Trend") displayLabel = "الاتجاه";
      if (label == "BB Status") displayLabel = "مؤشر بولينجر";
    }
    
    String displayValue = value;
    if (isAr) {
      if (value == "Overbought") displayValue = "تشبع شرائي";
      if (value == "Oversold") displayValue = "تشبع بيعي";
      if (value == "Neutral") displayValue = "محايد";
      if (value == "Bullish") displayValue = "صعودي";
      if (value == "Bearish") displayValue = "هبوطي";
    }

    return Column(
      children: [
        Text(displayLabel, style: const TextStyle(color: AppColors.textDim, fontSize: 10)),
        const SizedBox(height: 5),
        Text(displayValue, style: TextStyle(
          color: isDark ? Colors.white : Colors.black87, 
          fontWeight: FontWeight.bold, fontSize: 13)
        ),
      ],
    );
  }

  Widget _buildTabs(BuildContext context, AppProvider provider) {
    final isGold = provider.activeMetal == 'gold';
    final isAr = provider.locale.languageCode == 'ar';
    final isDark = provider.isDark;
    
    TextStyle getTabStyle(bool active) {
      // Fix Light Mode Text Visibility
      final inactiveColor = isDark ? Colors.white.withOpacity(0.9) : Colors.black54;
      final color = active ? Colors.black : inactiveColor;
      
      return GoogleFonts.cairo( 
        color: color,
        fontWeight: FontWeight.w900,
        fontSize: 32, 
        height: 1.2,
      );
    }

    return Container(
      padding: const EdgeInsets.all(5),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(50),
      ),
      child: Row(
        children: [
          Expanded(
            child: GestureDetector(
              onTap: () => provider.setActiveMetal('gold'),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                padding: const EdgeInsets.symmetric(vertical: 12),
                decoration: BoxDecoration(
                  color: isGold ? AppColors.primary : Colors.transparent,
                  borderRadius: BorderRadius.circular(40),
                  gradient: isGold 
                    ? const LinearGradient(colors: [AppColors.primaryLight, AppColors.primary])
                    : null,
                  boxShadow: isGold ? [BoxShadow(color: AppColors.primary.withOpacity(0.4), blurRadius: 15)] : [],
                ),
                child: Center(
                  child: Text(
                    isAr ? "ذهب" : "GOLD",
                    style: getTabStyle(isGold),
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            child: GestureDetector(
              onTap: () => provider.setActiveMetal('silver'),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                padding: const EdgeInsets.symmetric(vertical: 12),
                decoration: BoxDecoration(
                  color: !isGold ? AppColors.silver : Colors.transparent,
                  borderRadius: BorderRadius.circular(40),
                  gradient: !isGold 
                    ? const LinearGradient(colors: [Color(0xFFE0E0E0), AppColors.silver])
                    : null,
                  boxShadow: !isGold ? [BoxShadow(color: AppColors.silver.withOpacity(0.4), blurRadius: 15)] : [],
                ),
                child: Center(
                  child: Text(
                    isAr ? "فضة" : "SILVER",
                    style: getTabStyle(!isGold),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGridPrices(BuildContext context, AppProvider provider, Map<String, dynamic> data) {
    final isGold = provider.activeMetal == 'gold';
    final isAr = provider.locale.languageCode == 'ar';
    final isDark = provider.isDark;
    
    // Manual Calculation Logic (Safe Fallback)
    final metalData = isGold ? data['gold'] : data['silver'];
    double price24;
    if (isGold) {
      final priceOz = (metalData['egp']['price'] as num).toDouble();
      price24 = priceOz / 31.1034768;
    } else {
      final priceOz = (metalData['egp']['price'] as num).toDouble();
      price24 = priceOz / 31.1; // Use 31.1 for silver
    }

    List<Map<String, dynamic>> items = [];

    if (isGold) {
      items = [
        {"title": isAr ? "عيار ٢٤" : "24K", "price": price24},
        {"title": isAr ? "عيار ٢١" : "21K", "price": (price24 * 21) / 24},
        {"title": isAr ? "عيار ١٨" : "18K", "price": (price24 * 18) / 24},
      ];
    } else {
       final price999 = price24; // Silver usually quoted as 999
       items = [
        {"title": isAr ? "عيار ٩٩٩" : "999", "price": price999},
        {"title": isAr ? "عيار ٩٢٥" : "925", "price": price999 * 0.925},
        {"title": isAr ? "عيار ٨٠٠" : "800", "price": price999 * 0.800},
      ];
    }
    
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: items.map((item) {
        return Expanded(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 5),
            padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 10),
            decoration: BoxDecoration(
              color: isDark ? AppColors.cardBg : Colors.white,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: isDark ? Colors.white10 : Colors.black12),
            ),
            child: Column(
              children: [
                Text(
                  item['title'] as String,
                  style: GoogleFonts.outfit(
                      color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 18),
                ),
                const SizedBox(height: 10),
                Text(
                  NumberFormat("#,##0", "en_US").format(item['price']),
                  style: GoogleFonts.outfit(
                     fontSize: 22,
                     fontWeight: FontWeight.w800,
                     color: isDark ? Colors.white : Colors.black87
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  "EGP/g",
                  style: GoogleFonts.outfit(color: AppColors.textDim, fontSize: 12),
                ),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}
