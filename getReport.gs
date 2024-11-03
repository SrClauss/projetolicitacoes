function getReport() {
  const aDisputar = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("A Disputar 2.0");
  const line = 281;
  const fileId = aDisputar.getRange(line, 9).getValue().split("/d/")[1].split("/")[0];
  const fileBlob = DriveApp.getFileById(fileId).getBlob();

  const options = {
    method: 'post',
    contendType: 'multipart/form-data',
    headers: {
      'ngrok-skip-browser-warning': 'Valor-Do-Cabecalho'
    },
    payload: {
      'file': fileBlob
    }
  };

  Logger.log("Enviando arquivo para a IA");
  const response = UrlFetchApp.fetch("https://boss-squirrel-instantly.ngrok-free.app/uploadfile", options);
  const json = JSON.parse(response.getContentText());


  const docId = "1FZaVot_I__lLkIa-JIBd2-5LxIizTDA7Xev5X2DWERo"; // ID do documento modelo
  const folderId = "1T4Su32nq_PsTQdopywpyuy3ywqdMUdGI"; // ID da pasta 'Relatorios'

  // Copiar o documento modelo para a pasta 'Relatorios' com o novo nome
  const templateFile = DriveApp.getFileById(docId);
  const newName = json.orgao_licitante + " - " + json.pregao_eletronico;
  const copy = templateFile.makeCopy(newName, DriveApp.getFolderById(folderId));

  // Abrir o novo documento
  const newDoc = DocumentApp.openById(copy.getId());

  // Substituir os marcadores no novo documento
  Object.keys(json).forEach(key => {
    newDoc.getBody().replaceText("\\[" + key + "\\]", json[key]); // Escapar colchetes
  });

  newDoc.saveAndClose(); // Garantir que o documento seja salvo

  const destinyCell = aDisputar.getRange(line, 12);

  destinyCell.setValue(newDoc.getUrl())

}

