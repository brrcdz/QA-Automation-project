HOST = 127.0.0.1
PORT = 4000
process = $(shell ps -ef | grep ./tester.so | grep -v grep |  awk '{print $$2}')

app: # Поднять приложение на дефолтном порту
	./tester.so ${HOST} ${PORT} &

kill_app: # Убить приложение по PID
	kill $(process)

run_tests: # Запуск тестов
	pytest -vv

allure_tests: allure_clean # Запуск тестов с генерацией отчёта allure
	pytest -q --alluredir=allure

allure_report: # Генерация отчёта allure
	allure serve allure/

allure_clean: # Очистить папку с отчётом allure
	rm -rf allure

run: app run_tests kill_app # прогон тестов без генеации allure-report
run_allure: app allure_tests kill_app allure_report # прогон тестов с генерацией allure-report