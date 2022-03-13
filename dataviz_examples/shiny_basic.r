library(shiny)

ui <- fluidPage(    
  checkboxGroupInput("checkGroup1", label = h3("This is a Checkbox group"), 
                 choices = list("1" = 1, "2" = 2, "3" = 3),
                 selected = 1),
  fluidRow(column(3, verbatimTextOutput("text_choice")))
  ) 


server <- function(input, output){
  output$text_choice <- renderPrint({
    return(paste0("You have chosen the choice ",input$checkGroup1))})
} 

shinyApp(ui = ui, server = server)