"use client"

import { DashboardHeader } from "@/components/dashboard-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Send, Bot, User, Sparkles } from "lucide-react"
import { useState } from "react"

const suggestedPrompts = [
  "Quais são os novos prazos para a declaração do MEI?",
  "Como calcular o DAS mensal do MEI?",
  "Quais documentos preciso guardar para a declaração anual?",
  "Como emitir nota fiscal como MEI?",
]

const mockMessages = [
  {
    role: "assistant",
    content: "Olá! Sou o Agente Contábil especializado em MEI. Como posso ajudá-lo hoje?",
  },
]

export default function AccountingAgentPage() {
  const [messages, setMessages] = useState(mockMessages)
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim()) return

    setMessages([
      ...messages,
      { role: "user", content: input },
      {
        role: "assistant",
        content:
          "Entendo sua dúvida. Para a declaração do MEI em 2024, você precisa apresentar a DASN-SIMEI até 31 de maio. Os principais documentos necessários são: notas fiscais de compra e venda, recibos de despesas, e comprovantes de pagamento do DAS. Posso ajudar com mais alguma informação específica?",
      },
    ])
    setInput("")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background">
      <DashboardHeader />
      <main className="container py-8 md:py-12">
        <div className="max-w-5xl mx-auto space-y-6">
          <Card className="border-2 border-primary/20 shadow-sm">
            <CardHeader>
              <div className="flex items-center gap-4">
                <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-primary to-primary/70 flex items-center justify-center shadow-lg">
                  <Bot className="h-8 w-8 text-primary-foreground" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <CardTitle className="text-2xl">Agente Contábil</CardTitle>
                    <Badge variant="outline" className="bg-accent/10 text-accent border-accent/20">
                      <Sparkles className="h-3 w-3 mr-1" />
                      IA Especializada
                    </Badge>
                  </div>
                  <CardDescription className="text-base">
                    Especialista em contabilidade para MEI, processamento de documentos e declarações fiscais
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>

          {messages.length <= 1 && (
            <Card className="shadow-sm border-border/50">
              <CardHeader>
                <CardTitle className="text-lg">Perguntas Sugeridas</CardTitle>
                <CardDescription>Clique em uma pergunta para começar</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-3 sm:grid-cols-2">
                  {suggestedPrompts.map((prompt, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      className="justify-start text-left h-auto py-4 px-4 hover:bg-muted/50 transition-colors bg-transparent"
                      onClick={() => setInput(prompt)}
                    >
                      <span className="text-sm leading-relaxed">{prompt}</span>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          <Card className="min-h-[500px] flex flex-col shadow-sm border-border/50">
            <CardContent className="flex-1 p-6">
              <div className="space-y-6">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex gap-4 ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}
                  >
                    <div
                      className={`h-10 w-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm ${
                        message.role === "user"
                          ? "bg-gradient-to-br from-primary to-primary/70"
                          : "bg-gradient-to-br from-accent to-accent/70"
                      }`}
                    >
                      {message.role === "user" ? (
                        <User className="h-5 w-5 text-primary-foreground" />
                      ) : (
                        <Bot className="h-5 w-5 text-accent-foreground" />
                      )}
                    </div>
                    <div
                      className={`flex-1 rounded-xl p-4 ${
                        message.role === "user" ? "bg-primary text-primary-foreground ml-12" : "bg-muted mr-12"
                      }`}
                    >
                      <p className="text-sm leading-relaxed">{message.content}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>

            <div className="border-t p-4 bg-muted/30">
              <div className="flex gap-2">
                <Input
                  placeholder="Digite sua pergunta sobre contabilidade MEI..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSend()}
                  className="flex-1 h-11"
                />
                <Button onClick={handleSend} size="icon" className="flex-shrink-0 h-11 w-11 shadow-sm">
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-xs text-muted-foreground mt-2">Custo: ~10 tokens por mensagem • Saldo: 1,250 tokens</p>
            </div>
          </Card>
        </div>
      </main>
    </div>
  )
}
