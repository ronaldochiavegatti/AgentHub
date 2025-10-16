import { DashboardHeader } from "@/components/dashboard-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Coins, CreditCard, TrendingUp, ArrowUpRight, ArrowDownRight } from "lucide-react"

const tokenPackages = [
  {
    name: "Starter",
    tokens: 1000,
    price: "R$ 29,90",
    popular: false,
  },
  {
    name: "Professional",
    tokens: 5000,
    price: "R$ 129,90",
    popular: true,
    savings: "13% de desconto",
  },
  {
    name: "Business",
    tokens: 15000,
    price: "R$ 349,90",
    popular: false,
    savings: "22% de desconto",
  },
]

const transactions = [
  {
    id: 1,
    type: "purchase",
    description: "Compra de 5.000 tokens",
    amount: 5000,
    value: "R$ 129,90",
    date: "2024-01-10",
  },
  {
    id: 2,
    type: "usage",
    description: "Processamento de documento",
    amount: -50,
    value: "-",
    date: "2024-01-12",
  },
  {
    id: 3,
    type: "usage",
    description: "Consulta ao Agente Contábil",
    amount: -30,
    value: "-",
    date: "2024-01-13",
  },
  {
    id: 4,
    type: "usage",
    description: "Processamento de documento",
    amount: -50,
    value: "-",
    date: "2024-01-14",
  },
  {
    id: 5,
    type: "usage",
    description: "Consulta ao Agente Contábil",
    amount: -20,
    value: "-",
    date: "2024-01-15",
  },
]

export default function BillingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background">
      <DashboardHeader />
      <main className="container py-8 md:py-12">
        <div className="space-y-6">
          <div className="space-y-2">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Faturamento e Créditos</h1>
            <p className="text-muted-foreground text-lg">Gerencie seus tokens e histórico de transações</p>
          </div>

          <Card className="border-2 border-primary/20 shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg font-medium">Saldo Atual</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4">
                <div className="h-20 w-20 rounded-2xl bg-gradient-to-br from-accent/10 to-accent/5 flex items-center justify-center shadow-sm">
                  <Coins className="h-10 w-10 text-accent" />
                </div>
                <div>
                  <p className="text-5xl font-bold">1,250</p>
                  <p className="text-sm text-muted-foreground mt-1">tokens disponíveis</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-6 md:grid-cols-3">
            <Card className="shadow-sm border-border/50">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Uso este Mês</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">3,750</div>
                <p className="text-xs text-muted-foreground mt-1">tokens consumidos</p>
              </CardContent>
            </Card>

            <Card className="shadow-sm border-border/50">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Documentos Processados</CardTitle>
                <ArrowUpRight className="h-4 w-4 text-accent" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">75</div>
                <p className="text-xs text-muted-foreground mt-1">+12% vs mês anterior</p>
              </CardContent>
            </Card>

            <Card className="shadow-sm border-border/50">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Consultas ao Agente</CardTitle>
                <ArrowDownRight className="h-4 w-4 text-destructive" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">42</div>
                <p className="text-xs text-muted-foreground mt-1">-5% vs mês anterior</p>
              </CardContent>
            </Card>
          </div>

          <Card className="shadow-sm border-border/50">
            <CardHeader>
              <CardTitle className="text-xl">Comprar Tokens</CardTitle>
              <CardDescription className="text-base">Escolha o pacote ideal para suas necessidades</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-3">
                {tokenPackages.map((pkg) => (
                  <Card
                    key={pkg.name}
                    className={pkg.popular ? "border-2 border-primary shadow-lg" : "border shadow-sm"}
                  >
                    <CardHeader>
                      <div className="flex items-center justify-between mb-2">
                        <CardTitle className="text-xl">{pkg.name}</CardTitle>
                        {pkg.popular && <Badge className="bg-primary text-primary-foreground">Popular</Badge>}
                      </div>
                      <div className="space-y-1">
                        <p className="text-4xl font-bold">{pkg.price}</p>
                        <p className="text-sm text-muted-foreground">{pkg.tokens.toLocaleString("pt-BR")} tokens</p>
                        {pkg.savings && (
                          <Badge variant="outline" className="bg-accent/10 text-accent border-accent/20">
                            {pkg.savings}
                          </Badge>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <Button className="w-full shadow-sm" variant={pkg.popular ? "default" : "outline"}>
                        <CreditCard className="h-4 w-4 mr-2" />
                        Comprar
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-sm border-border/50">
            <CardHeader>
              <CardTitle className="text-xl">Histórico de Transações</CardTitle>
              <CardDescription className="text-base">Acompanhe suas compras e consumo de tokens</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-lg border overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-muted/50">
                      <TableHead className="font-semibold">Descrição</TableHead>
                      <TableHead className="font-semibold">Data</TableHead>
                      <TableHead className="text-right font-semibold">Tokens</TableHead>
                      <TableHead className="text-right font-semibold">Valor</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {transactions.map((transaction) => (
                      <TableRow key={transaction.id} className="hover:bg-muted/30 transition-colors">
                        <TableCell className="font-medium">{transaction.description}</TableCell>
                        <TableCell>{new Date(transaction.date).toLocaleDateString("pt-BR")}</TableCell>
                        <TableCell className="text-right">
                          <span
                            className={
                              transaction.type === "purchase" ? "text-accent font-semibold" : "text-muted-foreground"
                            }
                          >
                            {transaction.amount > 0 ? "+" : ""}
                            {transaction.amount.toLocaleString("pt-BR")}
                          </span>
                        </TableCell>
                        <TableCell className="text-right font-medium">{transaction.value}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
