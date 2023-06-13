using Random
using DelimitedFiles: writedlm, readdlm
using Statistics

using ProgressBars

function erdos_renyi(N::Int,p::Float64,seed::Int)
    rng = MersenneTwister(seed)
    nl = Dict{Int,Vector{Int32}}()
    for i in 1:N 
        nl[i] = []
    end
    nodes = Int32.(collect(1:N))
    for i in 1:N
        for j in i:N
            if rand(rng) < p
                push!(nl[i],j)
                push!(nl[j],i)
            end
        end
    end
    nl
end

function oscillators_a(N::Int,p::Float64,seed1::Int,seed2::Int)
    rng = MersenneTwister(seed2)
    
    ϵ = 1e-2
    δt = 1e-3

    nl = erdos_renyi(N,p,seed1)

    θ = zeros(N)
    θ_0 = rand(rng,N)

    θ .+= θ_0

    T = 10 ^ 7

    t1 = []
    M = []
    for t in 1:T
        idx_threshold = findall(θ .>= 1) # Índices i de los elementos de θ en los que que θ_i >= θ_thr
        for i in idx_threshold
            θ[nl[i]] += ϵ*θ[nl[i]]
        end
        idx_threshold = findall(θ .>= 1) # Índices i de los elementos de θ en los que que θ_i >= θ_thr, una vez que mandamos los pulsos
        θ[idx_threshold] .= 0
        if 1 in idx_threshold
            push!(M,mean(1 .- θ))
            push!(t1,δt*t)
        end
        θ .+= δt
    end
    data = hcat(t1,M)
    fname = "p$(p)_N$(N)_$((10*seed1)+seed2).txt"
    open(fname,"w") do io
        writedlm(io,data[1:3000,:])
    end
    #data
end

### MAIN ###

N = [100]
p = [0.05]

for n in N
    for p_ in p
        println("N=$n, p=$p_")
        for seed1 in tqdm(0:9)
            for seed2 in 0:9
                oscillators_a(n,p_,seed1,seed2)
            end
        end
    end
end
