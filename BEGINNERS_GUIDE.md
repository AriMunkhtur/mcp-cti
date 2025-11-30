# 🛡️ MCP CTI Dashboard - Beginner's Guide

## What Is This Dashboard?

Imagine you're a security guard protecting a building. You need to know:
- **Who's trying to break in?** (Threat actors)
- **What methods are they using?** (Attack techniques)
- **Which doors/windows are vulnerable?** (Your assets)

This dashboard is like a **security camera system for the internet**. It watches for cyber threats that could affect your computer systems and shows them to you in an easy-to-understand way.

---

## 🎯 The Big Picture

### What Does "CTI" Mean?
**CTI = Cyber Threat Intelligence**

Think of it like a weather forecast, but for cyber attacks:
- Weather forecast tells you: "It might rain tomorrow, bring an umbrella"
- CTI tells you: "Hackers are targeting WordPress sites, update your software"

### Where Does the Data Come From?
We use **AlienVault OTX** (Open Threat Exchange) - it's like a global neighborhood watch for the internet. Security researchers worldwide share information about:
- Malicious websites
- Hacker groups
- Software vulnerabilities
- Malware (viruses, ransomware, etc.)

---

## 📊 Dashboard Layout

### Top Section: Quick Stats (The "At-a-Glance" View)

When you open the dashboard, you see **4 big numbers**:

#### 1. 🎯 Total Threats
**What it means:** How many potential dangers match your systems  
**Example:** "38 threats" means we found 38 things that could affect you  
**Why it matters:** More threats = more things to investigate

#### 2. 📊 Avg Risk Score
**What it means:** How dangerous are these threats on average (0-10 scale)  
**Example:** "7.2/10" means these are pretty serious threats  
**Why it matters:** Higher score = more urgent to address

#### 3. 🚨 Critical
**What it means:** Number of "drop everything and fix this NOW" threats  
**Example:** "5 Critical" means 5 extremely dangerous threats  
**Why it matters:** These should be your top priority

#### 4. ⚠️ High
**What it means:** Number of "fix this soon" threats  
**Example:** "12 High" means 12 serious (but not critical) threats  
**Why it matters:** Handle these after Critical ones

---

## 📈 Main Charts

### Chart 1: Severity Distribution (Bar Chart)
**What it shows:** How threats are categorized by danger level

**Color coding:**
- 🔴 **Red (Critical)**: Extremely dangerous - like a fire alarm
- 🟠 **Orange (High)**: Very serious - like a smoke detector
- 🟡 **Yellow (Medium)**: Worth attention - like a warning light
- 🟢 **Green (Low)**: Minor concern - like a reminder

**How to read it:**
If you see a tall red bar, you have many critical threats to address immediately.

### Chart 2: Threat Types (Donut Chart)
**What it shows:** What kinds of threats you're facing

**Common types:**
- **CVE**: Known software vulnerabilities (like a broken lock)
- **FileHash**: Malicious files (like a virus signature)
- **Domain**: Dangerous websites (like a sketchy neighborhood)
- **IP Address**: Suspicious servers (like a suspicious vehicle)

**How to read it:**
If "CVE" is the biggest slice, most threats are software vulnerabilities you can patch.

---

## 🔍 The Three Analysis Tabs

### Tab 1: 📊 Score Analysis

#### Score Distribution (Histogram)
**What it shows:** How threat scores are spread out

**Example:**
- Lots of bars on the left (low scores) = mostly minor threats
- Lots of bars on the right (high scores) = many serious threats

#### References vs Score (Scatter Plot)
**What it shows:** How many people are talking about each threat vs. how dangerous it is

**Why it matters:**
- High references + high score = Well-known, serious threat
- Low references + high score = New, emerging threat (potentially more dangerous!)

### Tab 2: 🏷️ Tag Intelligence

#### Tag Cloud
**What it shows:** Most common keywords associated with threats

**Example tags:**
- "ransomware" - Malware that locks your files
- "phishing" - Fake emails trying to steal passwords
- "apt" - Advanced Persistent Threat (sophisticated hackers)
- "zero-day" - Brand new vulnerability (very dangerous!)

**How to use it:**
If you see "ransomware" appearing a lot, you know that's a trending attack method right now.

### Tab 3: 📅 Timeline

#### Threat Timeline (Line Chart)
**What it shows:** When threats were discovered over time

**How to read it:**
- Upward spike = Sudden increase in threats (maybe a new attack campaign)
- Flat line = Steady, normal threat level
- Different colored lines = Different severity levels

#### Recent Threats List
**What it shows:** The 5 most recently discovered threats

**Why it matters:** New threats might not have patches/fixes yet, so they're extra dangerous.

---

## ⚙️ Sidebar Controls (The Customization Panel)

### 🎯 Asset Management

**What are "Assets"?**
Assets are the computer systems you want to protect. Think of them like items in your house:
- Your laptop = Asset
- Your phone = Asset
- Your web server = Asset

**Why list them?**
The dashboard only shows threats that affect YOUR specific systems. If you don't use WordPress, you don't care about WordPress threats.

**How to use it:**

1. **View Current Assets:**
   - Click "📝 Edit Assets"
   - See your list (e.g., "PHP 8.1", "MySQL 5.7")

2. **Delete an Asset:**
   - Click the 🗑️ button next to it
   - Use this when you stop using that software

3. **Add a New Asset:**
   - Name: What you call it (e.g., "Web Server")
   - Software: What program it runs (e.g., "Apache")
   - Version: Which version (e.g., "2.4")
   - Click "➕ Add Asset"

**Example:**
You just installed PostgreSQL 15 on your database server:
- Name: "Database"
- Software: "PostgreSQL"
- Version: "15"

Now the dashboard will show PostgreSQL-related threats!

---

### 🌍 Focus Areas

These filters help you focus on specific types of threats.

#### Country/Region Filter
**What it does:** Shows only threats targeting specific countries

**Example use case:**
You type "Mongolia" and the dashboard shows only threats where:
- The threat name mentions Mongolia
- Tags include Mongolia
- The threat is known to target Mongolia

**Why you'd use it:**
- You work for a company in Mongolia
- You're researching geopolitical cyber threats
- You want to see if a specific region is being targeted

#### Campaign/Actor Filter
**What it does:** Shows threats from specific hacker groups

**Example use case:**
You type "APT28" (a Russian hacking group) and see only their activities.

**Common threat actors:**
- **APT28** (Fancy Bear) - Russian military hackers
- **Lazarus Group** - North Korean hackers
- **APT29** (Cozy Bear) - Russian intelligence hackers

**Why you'd use it:**
- Track a specific hacker group
- Research their tactics
- See if they're targeting your industry

#### Keywords Filter
**What it does:** Searches for specific attack types or technologies

**Example use cases:**
- Type "ransomware" → See all ransomware threats
- Type "phishing" → See all phishing campaigns
- Type "python" → See threats targeting Python applications

**Why you'd use it:**
Focus on the attack types most relevant to you.

---

### 📊 Display Controls

#### Show Low Severity
**What it does:** Includes/excludes minor threats

**When to turn it OFF:**
- You're overwhelmed with threats
- You only want to see serious issues

**When to turn it ON:**
- You want the complete picture
- You're doing research

#### Max Threats to Display
**What it does:** Limits how many threats you see (10-100)

**Why adjust it:**
- **Lower (10-20)**: Faster loading, focus on top threats
- **Higher (80-100)**: Complete view, thorough analysis

---

## 📋 Detailed Threat Feed (The Main Table)

This is where you see ALL the details about each threat.

### Table Columns Explained:

#### Severity
🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

#### Risk Score
A progress bar showing danger level (0-10)
- 0-3: Low risk
- 4-6: Medium risk
- 7-8: High risk
- 9-10: Critical risk

#### Threat Name
What the threat is called
**Example:** "Exploit targeting PHP 8.1 in Web Server"

#### Type
What kind of indicator this is
**Examples:**
- CVE = Software vulnerability
- FileHash = Malicious file
- Domain = Bad website
- IPv4 = Suspicious IP address

#### Indicator
The actual technical detail
**Examples:**
- CVE-2024-1234 (vulnerability ID)
- malicious-site.com (bad domain)
- 192.168.1.1 (suspicious IP)

#### Tags
Keywords describing the threat
**Examples:** ["ransomware", "windows", "exploit"]

#### Date
When this threat was first reported

#### Refs
How many security researchers are tracking this
- High number = Well-known, verified threat
- Low number = New or less common

### Table Filters

Above the table, you can filter by:
1. **Severity**: Only show Critical and High
2. **Type**: Only show CVEs
3. **Minimum Risk Score**: Only show threats above 7.0

---

## 💾 Export Feature

**What it does:** Downloads all filtered threats as a CSV file

**Why you'd use it:**
- Share with your team
- Create reports for management
- Analyze in Excel/Google Sheets
- Keep records for compliance

**How to use it:**
1. Apply your filters
2. Click "📥 Download CSV"
3. File saves with timestamp (e.g., `threats_20241124_152211.csv`)

---

## 🎓 Real-World Scenarios

### Scenario 1: You're a Web Developer

**Your assets:**
- PHP 8.1
- MySQL 5.7
- WordPress 6.2

**How to use the dashboard:**
1. Add these to Asset Management
2. Check dashboard daily
3. If you see Critical threats for WordPress → Update immediately
4. Export monthly reports for your boss

### Scenario 2: You're Researching APT Groups

**Your goal:** Track Russian hacker groups

**How to use the dashboard:**
1. Campaign/Actor filter: "APT28, APT29, Fancy Bear"
2. Check Timeline tab to see activity patterns
3. Look at Tags to understand their methods
4. Export data for your research paper

### Scenario 3: You Work for a Company in Mongolia

**Your goal:** Monitor threats targeting your region

**How to use the dashboard:**
1. Country/Region filter: "Mongolia"
2. Check if threat activity is increasing (Timeline)
3. See what attack methods are being used (Tags)
4. Share Critical threats with IT team

---

## 🔑 Key Concepts to Remember

### 1. **Risk Score vs. Severity**
- **Risk Score**: Calculated number (0-10) based on multiple factors
- **Severity**: Category (Low/Medium/High/Critical) based on the score

### 2. **References Matter**
More references = More people have verified this threat = More trustworthy

### 3. **Tags Are Your Friend**
Tags help you quickly understand what kind of attack it is without reading technical details.

### 4. **Fresh Threats Are Dangerous**
New threats (recent dates) might not have fixes yet, so they're extra risky.

### 5. **Context Is Everything**
A "Critical" threat for WordPress doesn't matter if you don't use WordPress. That's why asset management is crucial!

---

## 🚀 Getting Started Checklist

- [ ] **Step 1:** Add your assets in the sidebar
- [ ] **Step 2:** Check the top metrics - how many threats?
- [ ] **Step 3:** Look at the severity chart - mostly Critical or Low?
- [ ] **Step 4:** Check the Tag Cloud - what attack types are trending?
- [ ] **Step 5:** Review the threat table - read the top 5 threats
- [ ] **Step 6:** Export data if you need to share with someone
- [ ] **Step 7:** Set up filters for your specific interests

---

## ❓ Common Questions

**Q: Why do I see so many threats?**  
A: The internet is a dangerous place! Not all threats will affect you - that's why asset filtering is important.

**Q: Should I panic if I see Critical threats?**  
A: No! Check if they actually affect YOUR systems. If yes, then take action calmly.

**Q: How often should I check this dashboard?**  
A: Daily for production systems, weekly for personal projects.

**Q: What if I don't understand a threat?**  
A: Look at the tags first - they give you the general idea. Then Google the CVE number or threat name for more info.

**Q: Can I trust this data?**  
A: OTX is a reputable source used by security professionals worldwide. However, always verify critical threats with additional sources.

---

## 🎯 Next Steps

Now that you understand the dashboard:

1. **Practice:** Add some test assets and see how the threats change
2. **Explore:** Try different filters and see what you discover
3. **Learn:** When you see a threat, research it to understand it better
4. **Share:** Show your classmates or colleagues how it works

Remember: **Cybersecurity is about staying informed, not being scared!** This dashboard helps you stay one step ahead of the bad guys. 🛡️

---

## 📚 Glossary

- **APT**: Advanced Persistent Threat - Sophisticated, long-term hacking campaign
- **CVE**: Common Vulnerabilities and Exposures - Official ID for security bugs
- **Indicator**: A piece of data that suggests malicious activity
- **OTX**: Open Threat Exchange - Community threat intelligence platform
- **Pulse**: A collection of threat indicators shared on OTX
- **Ransomware**: Malware that encrypts your files and demands payment
- **Zero-day**: A vulnerability that's being exploited before a fix exists

---

**Happy Threat Hunting! 🕵️‍♂️**
