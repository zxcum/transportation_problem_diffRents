// Получаем элементы таблицы
var table = document.getElementById('data-table');

// Получаем кнопки для добавления столбцов и строк
var addColumnBtn = document.getElementById('add-column-btn');
var addRowBtn = document.getElementById('add-row-btn');

// Обработчик клика по кнопке "Добавить столбец"
addColumnBtn.addEventListener('click', function() {
  var lastColumnIndex = table.rows[0].cells.length - 1;
  var newRow = table.insertRow();
  
  for (var i = 0; i < table.rows.length; i++) {
    var cell = newRow.insertCell();
    if (i === 0) {
      cell.innerHTML = '<input type="text" class="column" placeholder="B' + (lastColumnIndex + 1) + '">';
    } else {
      cell.innerHTML = '<input type="text" class="data" placeholder="Введите значение">';
    }
  }
});

// Обработчик клика по кнопке "Добавить строку"
addRowBtn.addEventListener('click', function() {
  var lastRowIndex = table.rows.length - 1;
  var newRow = table.insertRow();
  
  for (var i = 0; i < table.rows[0].cells.length; i++) {
    var cell = newRow.insertCell();
    if (i === 0) {
      cell.innerHTML = '<input type="text" class="row" placeholder="A' + (lastRowIndex + 1) + '">';
    } else if (i === table.rows[0].cells.length - 1) {
      cell.innerHTML = 'Запасы';
    } else {
      cell.innerHTML = '<input type="text" class="data" placeholder="Введите значение">';
    }
  }
});
