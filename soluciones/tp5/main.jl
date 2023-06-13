using Random
using StatsBase
using DelimitedFiles: writedlm, readdlm
using ProgressBars

function WS_1D(N::Int,p::Float64,seed::Int)
    rng = MersenneTwister(seed) # Generador de números aleatorios inicializado con semilla
    nl = Dict{Int,Vector{Int32}}() 
    for i in 2:N-1 # Configuración inicial
        nl[i] = []
        push!(nl[i],i-1,i+1)
    end
    # Condiciones periódicas
    nl[1] = [2,N]
    nl[N] = [1,N-1]
    nodes = collect(1:N)
    # Sorteamos los enlaces nuevos
    for i in 1:N
        if rand(rng) < p
            j = i
            while i==j
                j = rand(rng,nodes,1)[1]
            end
            push!(nl[i],j)
            push!(nl[j],i)
        end
    end
    nl
end

function get_E(nl::Dict{Int,Vector{Int32}},spins::Vector{Int8},i::Int)
    E0 = - sum(spins[i] * spins[j] for j in nl[i])
    E  = - sum((-spins[i]) * spins[j] for j in nl[i])
    E - E0
end

function Ising(N::Int,p::Float64,t::Int,seed::Int)
    rng = MersenneTwister(seed)
    nl = WS_1D(N,p,seed)
    spins = sample(rng,[-1,1],N)
    spins = convert(Vector{Int8},spins)
    nodes = collect(1:N)
    for t in tqdm(1:t)
        i = rand(rng,nodes,1)[1]
        ΔE = get_E(nl,spins,i)
        if ΔE < 0
            spins[i] = - spins[i]
        elseif ΔE == 0
            if rand(rng) < 0.5
                spins[i] = - spins[i]
            end
        end
    end
    fname = "ising_$p"
    open(fname,"w") do io
        writedlm(io,spins)
    end
    spins
end

N = 10000
t = 10^10

p = 0.01
Ising(N,p,t,42)

p = 0.02
Ising(N,p,t,42)

p = 0.04
Ising(N,p,t,42)

p = 0.06
Ising(N,p,t,42)

p = 0.1
Ising(N,p,t,42)
