Перем ы;

Функция Факториал(Знач ч)
    Если ч = 0 ИЛИ ч = 1 Тогда
        Возврат 1;
    Иначе
        Возврат ч * Факториал(ч - 1);
    КонецЕсли
КонецФункции

ы = 10;
Сообщить("Факториал " + ы + " равен " + Факториал(ы));
