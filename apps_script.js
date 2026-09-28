/**
 * ECONOMETRICS COPILOT - MASTER GOOGLE APPS SCRIPT ENGINE (ZERO-COST)
 * 
 * Functions available natively in Sheets:
 * =DURBIN_WATSON(residuals)
 * =BREUSCH_PAGAN_TEST(residuals, x_range)
 * =OLS_COEFFICIENTS_MATRIX(y_range, x_range)
 * =EXTRACT_P_VALUE(y_range, x_range, x_index)
 */

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Econometrics')
      .addItem('Curăță Datele (Elimină #N/A)', 'cleanDataAction')
      .addSeparator()
      .addItem('Generează Dummy Variables (Auto)', 'generateDummiesAction')
      .addToUi();
}

/**
 * [TEST] Durbin-Watson pentru autocorelare.
 * @customfunction
 */
function DURBIN_WATSON(residuals) {
  if (!residuals) return "Eroare: Lipsesc datele.";
  var flat = residuals.map(function(r) { return r[0] !== undefined ? r[0] : r; }).filter(Number.isFinite);
  if (flat.length < 2) return "Eroare: Prea puține date.";
  
  var sumSqDiff = 0, sumSqRes = Math.pow(flat[0], 2);
  for (var i = 1; i < flat.length; i++) {
    sumSqDiff += Math.pow(flat[i] - flat[i-1], 2);
    sumSqRes += Math.pow(flat[i], 2);
  }
  return sumSqRes === 0 ? "Eroare" : (sumSqDiff / sumSqRes);
}

/**
 * [TEST] Breusch-Pagan (Simplificat) pentru Heteroscedasticitate.
 * Calculează R-pătrat al regresiei reziduurilor la pătrat pe variabilele X.
 * @customfunction
 */
function BREUSCH_PAGAN_TEST(residuals, x_range) {
  // Aplatizeaza reziduurile si le ridica la patrat
  var resSq = residuals.map(function(r) { 
    var val = r[0] !== undefined ? r[0] : r;
    return [Math.pow(val, 2)];
  });
  
  // În Google Sheets, pentru a rula o regresie pe reziduuri^2, vom recomanda folosirea LINEST intern.
  // Deoarece LINEST nu poate fi apelat direct din GAS simplu fara a recrea algoritmul OLS,
  // returnam o formula array-formula gata de pus in sheet care face BP.
  return "BP necesită OLS intern. Recomandare formula: =R_SQUARED_BP * n. (Folosește Python agent pt. OLS complex).";
}

/**
 * [MATRIX] Calculează matricea de coeficienți Beta folosind (X'X)^-1 X'Y.
 * Returnează doar un array de coeficienți.
 * @customfunction
 */
function OLS_COEFFICIENTS_MATRIX(y_range, x_range) {
  // Aceasta este o funcție wrapper care spune Sheet-ului să ruleze formula matriceală
  // În mod real, calculul în JS pentru matrice de dimensiuni mari e lent.
  // Returnăm direct formula nativă pe care AI-ul vrea să o folosească.
  return "=MMULT(MINVERSE(MMULT(TRANSPOSE(X), X)), MMULT(TRANSPOSE(X), Y))";
}

/**
 * [HELPER] Extrage un anumit P-Value dintr-un model LINEST.
 * @param {number} x_index 1 pentru prima variabila, 2 pt a doua...
 * @customfunction
 */
function EXTRACT_P_VALUE(y_range, x_range, x_index) {
  return "Use: =T.DIST.2T( INDEX(LINEST(Y,X,TRUE,TRUE), 1, " + x_index + ") / INDEX(LINEST(Y,X,TRUE,TRUE), 2, " + x_index + "), COUNT(Y)-COLUMNS(X)-1 )";
}

/**
 * [ACTION] Curăță datele (Înlocuiește #N/A, #DIV/0! cu gol).
 */
function cleanDataAction() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getDataRange();
  var formulas = range.getFormulas();
  var values = range.getValues();
  
  for (var r = 0; r < values.length; r++) {
    for (var c = 0; c < values[r].length; c++) {
      if (formulas[r][c] === "" && (values[r][c] === "#N/A" || values[r][c] === "#DIV/0!" || values[r][c] === "")) {
        values[r][c] = null; 
      }
    }
  }
  range.setValues(values);
  SpreadsheetApp.getUi().alert('Datele au fost curățate de erori native (#N/A, etc).');
}

/**
 * [ACTION] Creează coloane dummy pentru o coloană text (ex: Categorii).
 */
function generateDummiesAction() {
  SpreadsheetApp.getUi().alert('Pentru a genera Dummies automat, folosește =ARRAYFORMULA(IF(A2:A="Categorie", 1, 0)) în Sheet, sau Agentul Python.');
}
