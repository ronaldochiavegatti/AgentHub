"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles } from "lucide-react"

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    localStorage.setItem("isAuthenticated", "true")
    localStorage.setItem("userEmail", email || "demo@agenthub.com")
    localStorage.setItem("userName", "João Silva")
    router.push("/dashboard")
  }

  const handleDemoLogin = () => {
    localStorage.setItem("isAuthenticated", "true")
    localStorage.setItem("userEmail", "demo@agenthub.com")
    localStorage.setItem("userName", "João Silva")
    router.push("/dashboard")
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-muted/30 to-background p-4">
      <Card className="w-full max-w-md shadow-xl border-border/50">
        <CardHeader className="space-y-3 text-center pb-6">
          <div className="flex justify-center mb-2">
            <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-primary to-primary/70 flex items-center justify-center shadow-lg">
              <Sparkles className="h-7 w-7 text-primary-foreground" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold tracking-tight">Bem-vindo de volta</CardTitle>
          <CardDescription className="text-base">Entre com suas credenciais para acessar a plataforma</CardDescription>
        </CardHeader>
        <form onSubmit={handleLogin}>
          <CardContent className="space-y-5">
            <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
              <p className="text-sm font-semibold text-primary mb-2">Credenciais de Teste:</p>
              <p className="text-sm text-muted-foreground">Email: demo@agenthub.com</p>
              <p className="text-sm text-muted-foreground">Senha: qualquer senha</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-11"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-sm font-medium">
                Senha
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-11"
              />
            </div>
            <div className="flex items-center justify-end">
              <Link
                href="/forgot-password"
                className="text-sm text-primary hover:underline font-medium transition-colors"
              >
                Esqueceu sua senha?
              </Link>
            </div>
            <Button type="submit" className="w-full h-11 font-medium shadow-sm" size="lg">
              Entrar
            </Button>
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Ou</span>
              </div>
            </div>
            <Button
              type="button"
              variant="outline"
              className="w-full h-11 font-medium bg-transparent"
              size="lg"
              onClick={handleDemoLogin}
            >
              Entrar com Conta Demo
            </Button>
          </CardContent>
        </form>
        <CardFooter className="flex justify-center pt-2">
          <p className="text-sm text-muted-foreground">
            Não tem uma conta?{" "}
            <Link href="/register" className="text-primary hover:underline font-semibold transition-colors">
              Cadastre-se
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}
