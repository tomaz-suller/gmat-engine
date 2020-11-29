function Criar_Forms() 
{
  var form = FormApp.openByUrl('https://docs.google.com/forms/d/1YxqySiyKrF3gM4OHv7n5TmG4eIotht2i1VC5-sPUz9k/edit');

  form.addPageBreakItem()
  .setTitle('GMAT').setHelpText('Esta prova deve ser realizada até o dia 22/11 (Domingo).\nEla possui 10 questões de PST retiradas de 1 simulado da McKinsey.\nTempo recomendado para a realização da prova: 30 minutos.');
  
  var item = form.addMultipleChoiceItem();
  
  item.setTitle('Qual seu nome?');
  
  item.setChoices([
    item.createChoice('Alejandro Merino'),
    item.createChoice('André Stiernet'),
    item.createChoice('Camila Gabriades'),
    item.createChoice('David Guevara'),
    item.createChoice('Gabriel Paganini'),
    item.createChoice('Halef Michel'),
    item.createChoice('José Pedro Faustino'),
    item.createChoice('João Gubitoso'),
    item.createChoice('Marcelo Okada'),
    item.createChoice('Matheus Chiang'),
    item.createChoice('Matias Cardoso'),
    item.createChoice('Pedro Lin'),
    item.createChoice('Ricardo Arruda'),
    item.createChoice('Tomaz Suller'),
    item.createChoice('Victor Paschoalini')
  ]);
  
 
  form.addPageBreakItem()
  .setTitle('Questões').setHelpText('Esta prova deve ser realizada até o dia 22/11 (Domingo).\nEla possui 10 questões de PST retiradas de 1 simulado da McKinsey.\nTempo recomendado para a realização da prova: 30 minutos.');
  
  var item = form.addMultipleChoiceItem();
  
  item.setTitle('Qual meu nome?');
  
  item.setChoices([
    item.createChoice('Alejandro Merino', true),
    item.createChoice('André Stiernet'),
    item.createChoice('Camila Gabriades'),
    item.createChoice('David Guevara'),
    item.createChoice('Gabriel Paganini'),
    item.createChoice('Halef Michel'),
    item.createChoice('José Pedro Faustino'),
    item.createChoice('João Gubitoso'),
    item.createChoice('Marcelo Okada'),
    item.createChoice('Matheus Chiang'),
    item.createChoice('Matias Cardoso'),
    item.createChoice('Pedro Lin'),
    item.createChoice('Ricardo Arruda'),
    item.createChoice('Tomaz Suller'),
    item.createChoice('Victor Paschoalini')
  ]);

  var item = form.addMultipleChoiceItem();
  
  item.setTitle('Qual o nome?');
  
  item.setPoints(1)
  
  item.setChoices([
    item.createChoice('Alejandro Merino'),
    item.createChoice('André Stiernet', true),
    item.createChoice('Camila Gabriades'),
    item.createChoice('David Guevara'),
    item.createChoice('Gabriel Paganini'),
    item.createChoice('Halef Michel'),
    item.createChoice('José Pedro Faustino'),
    item.createChoice('João Gubitoso'),
    item.createChoice('Marcelo Okada'),
    item.createChoice('Matheus Chiang'),
    item.createChoice('Matias Cardoso'),
    item.createChoice('Pedro Lin'),
    item.createChoice('Ricardo Arruda'),
    item.createChoice('Tomaz Suller'),
    item.createChoice('Victor Paschoalini')
  ]);
  
  Logger.log('Published URL: ' + form.getPublishedUrl());
  
  Logger.log('Editor URL: ' + form.getEditUrl());
}