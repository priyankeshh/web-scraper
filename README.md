# 🌐 Web Scraper with Streamlit Interface

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent web scraping tool that combines the power of Selenium automation with a user-friendly Streamlit interface. Extract, process, and visualize web data effortlessly.

## ✨ Features

- 🤖 Automated web scraping using Selenium
- 📊 Interactive data visualization with Streamlit
- 💾 Multiple export formats (JSON, Excel, Markdown)
- 🔄 Real-time progress tracking
- 🎯 Customizable scraping parameters
- 📱 Responsive web interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Chrome browser version 132 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/priyankeshh/web-scraper.git
cd web-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Start the application:
```bash
streamlit run streamlit_app.py
```

2. Enter the target URL in the web interface
3. Configure scraping parameters
4. Click 'Start Scraping' to begin

## 📸 Example Usage

### 1. Target Website
<!-- Insert screenshot of the target website here -->
*Screenshot of the website we want to scrape data from*

### 2. Configuration
<!-- Insert screenshot of the scraper interface with configuration -->
*Screenshot showing how to configure the scraper with your desired fields*

### 3. Scraping Results
<!-- Insert screenshot of the scraped data in the app -->
*Screenshot showing the successfully scraped data in the application*

### 4. Exported Data
<!-- Insert screenshot of the exported CSV file -->
*Screenshot showing the final structured data in CSV format*

Example of scraping train schedule information:
```json
{
  "listings": [
    {
      "train_number": "12345",
      "train_name": "Express",
      "departure": "10:00 AM",
      "arrival": "06:30 PM",
      "duration": "8h 30m"
    }
  ]
}
```

This section demonstrates the complete workflow from selecting a target website to obtaining structured, usable data.

## 🛠️ Technical Stack

- **Web Automation**: Selenium WebDriver
- **Data Processing**: Pandas
- **User Interface**: Streamlit
- **Data Export**: OpenPyXL, JSON
- **Browser Driver**: ChromeDriver

## 📁 Project Structure

```
web-scraper/
│
├── streamlit_app.py    # Main Streamlit interface
├── scraper.py         # Core scraping logic
├── assets.py         # Utility functions
├── requirements.txt  # Project dependencies
├── output/          # Scraped data storage
└── chromedriver-win64/ # Chrome WebDriver
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

Made with ❤️ by Priyankesh
- GitHub: [@priyankeshh](https://github.com/priyankeshh)

## 🙏 Acknowledgments

- Selenium Documentation
- Streamlit Community
- ChromeDriver team
