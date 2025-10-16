import { DashboardHeader } from "@/components/dashboard-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Download, FileText, CheckCircle, Copy } from "lucide-react"
import Link from "next/link"

export default function DocumentDetailPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background">
      <DashboardHeader />
      <main className="container py-8 md:py-12">
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Link
                  href="/documents"
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  Documentos
                </Link>
                <span className="text-muted-foreground">/</span>
                <span className="text-sm font-medium">Nota Fiscal 2024-001.pdf</span>
              </div>
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Detalhes do Documento</h1>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <Button variant="outline" size="sm" className="shadow-sm bg-transparent">
                <Copy className="h-4 w-4 mr-2" />
                Copiar Dados
              </Button>
              <Button variant="outline" size="sm" className="shadow-sm bg-transparent">
                <Download className="h-4 w-4 mr-2" />
                Exportar Excel
              </Button>
              <Button variant="outline" size="sm" className="shadow-sm bg-transparent">
                <Download className="h-4 w-4 mr-2" />
                Exportar CSV
              </Button>
            </div>
          </div>

          <Card className="shadow-sm border-border/50">
            <CardHeader>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center shadow-sm">
                    <FileText className="h-7 w-7 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-xl">Nota Fiscal 2024-001.pdf</CardTitle>
                    <CardDescription className="text-base">Processado em 15 de janeiro de 2024</CardDescription>
                  </div>
                </div>
                <Badge variant="outline" className="bg-accent/10 text-accent border-accent/20 w-fit">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Concluído
                </Badge>
              </div>
            </CardHeader>
          </Card>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card className="lg:sticky lg:top-24 h-fit shadow-sm border-border/50">
              <CardHeader>
                <CardTitle className="text-xl">Documento Original</CardTitle>
                <CardDescription>Visualização do arquivo enviado</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="aspect-[3/4] bg-muted rounded-xl flex items-center justify-center border overflow-hidden">
                  <img
                    src="/nota-fiscal-brasileira-documento-contabil.jpg"
                    alt="Documento"
                    className="w-full h-full object-contain rounded-xl"
                  />
                </div>
              </CardContent>
            </Card>

            <Card className="shadow-sm border-border/50">
              <CardHeader>
                <CardTitle className="text-xl">Dados Extraídos</CardTitle>
                <CardDescription>Informações processadas pela IA</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="font-semibold text-lg mb-3">Informações do Emissor</h3>
                  <div className="space-y-3">
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Razão Social:</span>
                      <span className="text-sm font-medium col-span-2">Empresa XYZ Ltda</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">CNPJ:</span>
                      <span className="text-sm font-medium col-span-2">12.345.678/0001-90</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Endereço:</span>
                      <span className="text-sm font-medium col-span-2">Rua das Flores, 123 - São Paulo, SP</span>
                    </div>
                  </div>
                </div>

                <Separator />

                <div>
                  <h3 className="font-semibold text-lg mb-3">Informações da Nota Fiscal</h3>
                  <div className="space-y-3">
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Número:</span>
                      <span className="text-sm font-medium col-span-2">2024-001</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Data de Emissão:</span>
                      <span className="text-sm font-medium col-span-2">10/01/2024</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Chave de Acesso:</span>
                      <span className="text-sm font-medium col-span-2 break-all">
                        1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234
                      </span>
                    </div>
                  </div>
                </div>

                <Separator />

                <div>
                  <h3 className="font-semibold text-lg mb-3">Itens da Nota</h3>
                  <div className="border rounded-xl overflow-hidden">
                    <table className="w-full text-sm">
                      <thead className="bg-muted/50">
                        <tr>
                          <th className="text-left p-3 font-semibold">Descrição</th>
                          <th className="text-right p-3 font-semibold">Qtd</th>
                          <th className="text-right p-3 font-semibold">Valor Unit.</th>
                          <th className="text-right p-3 font-semibold">Total</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr className="border-t hover:bg-muted/30 transition-colors">
                          <td className="p-3">Serviço de Consultoria</td>
                          <td className="text-right p-3">1</td>
                          <td className="text-right p-3">R$ 2.500,00</td>
                          <td className="text-right p-3 font-medium">R$ 2.500,00</td>
                        </tr>
                        <tr className="border-t hover:bg-muted/30 transition-colors">
                          <td className="p-3">Taxa de Administração</td>
                          <td className="text-right p-3">1</td>
                          <td className="text-right p-3">R$ 350,00</td>
                          <td className="text-right p-3 font-medium">R$ 350,00</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <Separator />

                <div>
                  <h3 className="font-semibold text-lg mb-3">Valores Totais</h3>
                  <div className="space-y-3">
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Subtotal:</span>
                      <span className="text-sm font-medium col-span-2">R$ 2.850,00</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <span className="text-sm text-muted-foreground">Impostos:</span>
                      <span className="text-sm font-medium col-span-2">R$ 150,00</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 pt-2 border-t">
                      <span className="text-sm font-semibold">Total:</span>
                      <span className="text-2xl font-bold col-span-2 text-primary">R$ 3.000,00</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
