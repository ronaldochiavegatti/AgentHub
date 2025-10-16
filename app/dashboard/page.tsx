"use client"

import { useEffect, useState } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, MessageSquare, Upload, CheckCircle, Clock, AlertCircle, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function DashboardPage() {
  const [userName, setUserName] = useState("Usuário")

  useEffect(() => {
    const name = localStorage.getItem("userName")
    if (name) setUserName(name.split(" ")[0])
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background">
      <DashboardHeader />
      <main className="container py-8 md:py-12">
        <div className="space-y-8">
          <div className="space-y-2">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Olá, {userName}!</h1>
            <p className="text-muted-foreground text-lg">Bem-vindo de volta à sua plataforma de agentes de IA</p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <Link href="/documents" className="group">
              <Card className="transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5 border-border/50 h-full">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center group-hover:from-primary/20 group-hover:to-primary/10 transition-all duration-200 shadow-sm">
                      <Upload className="h-7 w-7 text-primary" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-1">Enviar Novo Documento</CardTitle>
                      <CardDescription className="text-base">
                        Faça upload de notas fiscais e documentos contábeis
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            </Link>

            <Link href="/agent/accounting" className="group">
              <Card className="transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5 border-border/50 h-full">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-accent/10 to-accent/5 flex items-center justify-center group-hover:from-accent/20 group-hover:to-accent/10 transition-all duration-200 shadow-sm">
                      <MessageSquare className="h-7 w-7 text-accent" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-1">Falar com Agente Contábil</CardTitle>
                      <CardDescription className="text-base">
                        Tire dúvidas sobre impostos e declarações MEI
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            </Link>
          </div>

          <Card className="shadow-sm border-border/50">
            <CardHeader className="pb-4">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl">Atividade Recente</CardTitle>
                  <CardDescription className="text-base mt-1">
                    Acompanhe o processamento dos seus documentos
                  </CardDescription>
                </div>
                <TrendingUp className="h-5 w-5 text-muted-foreground" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-4 p-4 rounded-xl border bg-card hover:bg-muted/50 transition-colors cursor-pointer">
                  <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-accent/10 to-accent/5 flex items-center justify-center flex-shrink-0 shadow-sm">
                    <CheckCircle className="h-5 w-5 text-accent" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-sm">Nota Fiscal 2024-001.pdf</p>
                    <p className="text-sm text-muted-foreground">Processado com sucesso</p>
                  </div>
                  <div className="text-sm text-muted-foreground font-medium">Há 2 horas</div>
                </div>

                <div className="flex items-center gap-4 p-4 rounded-xl border bg-card hover:bg-muted/50 transition-colors cursor-pointer">
                  <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center flex-shrink-0 shadow-sm">
                    <Clock className="h-5 w-5 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-sm">Recibo-Pagamento-Jan.pdf</p>
                    <p className="text-sm text-muted-foreground">Processando...</p>
                  </div>
                  <div className="text-sm text-muted-foreground font-medium">Há 5 horas</div>
                </div>

                <div className="flex items-center gap-4 p-4 rounded-xl border bg-card hover:bg-muted/50 transition-colors cursor-pointer">
                  <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-accent/10 to-accent/5 flex items-center justify-center flex-shrink-0 shadow-sm">
                    <CheckCircle className="h-5 w-5 text-accent" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-sm">Despesas-Dezembro-2023.xlsx</p>
                    <p className="text-sm text-muted-foreground">Processado com sucesso</p>
                  </div>
                  <div className="text-sm text-muted-foreground font-medium">Ontem</div>
                </div>

                <div className="flex items-center gap-4 p-4 rounded-xl border bg-card hover:bg-muted/50 transition-colors cursor-pointer">
                  <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-destructive/10 to-destructive/5 flex items-center justify-center flex-shrink-0 shadow-sm">
                    <AlertCircle className="h-5 w-5 text-destructive" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-sm">Documento-Ilegivel.jpg</p>
                    <p className="text-sm text-muted-foreground">Erro no processamento</p>
                  </div>
                  <div className="text-sm text-muted-foreground font-medium">Há 2 dias</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Active Agents */}
          <Card className="shadow-sm border-border/50">
            <CardHeader className="pb-4">
              <CardTitle className="text-2xl">Seus Agentes Ativos</CardTitle>
              <CardDescription className="text-base mt-1">Agentes de IA disponíveis para você</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <Card className="border-2 border-primary/20 shadow-md transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center shadow-sm">
                        <FileText className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">Agente Contábil</CardTitle>
                        <CardDescription className="text-xs font-medium text-accent">Ativo</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      Processamento de documentos fiscais e consultoria sobre declarações MEI
                    </p>
                    <Button asChild className="w-full shadow-sm" size="sm">
                      <Link href="/agent/accounting">Acessar Agente</Link>
                    </Button>
                  </CardContent>
                </Card>

                <Card className="border-2 border-dashed opacity-60">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="h-12 w-12 rounded-xl bg-muted flex items-center justify-center">
                        <FileText className="h-6 w-6 text-muted-foreground" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">Mais Agentes</CardTitle>
                        <CardDescription className="text-xs font-medium">Em breve</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      Novos agentes especializados serão adicionados em breve
                    </p>
                    <Button variant="outline" className="w-full bg-transparent" size="sm" disabled>
                      Em Desenvolvimento
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
