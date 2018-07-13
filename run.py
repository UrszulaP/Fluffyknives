from app_files import app

if __name__ == '__main__':
	app.run(debug=True, use_debugger=False)

# Przy publikowaniu aplikacji należy wyłączyć debug mode
# Względy bezpieczeństwa, przy powstaniu błędu użytkownicy nie będą mieli
# wyświetlonych informacji o błędzie (ścieżek i fragmentów kodu)