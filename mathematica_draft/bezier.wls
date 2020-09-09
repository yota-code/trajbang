#!/usr/bin/env wolframscript

x[t_] := p0x*(1-t)^7 + p1x*7*t^1*(1-t)^6 + p2x*21*t^2*(1-t)^5 + p3x*35*t^3*(1-t)^4 + p4x*35*t^4*(1-t)^3 + p5x*21*t^5*(1-t)^2 + p6x*7*t^6*(1-t)^1 + p7x*t^7

y[t_] := p0y*(1-t)^7 + p1y*7*t^1*(1-t)^6 + p2y*21*t^2*(1-t)^5 + p3y*35*t^3*(1-t)^4 + p4y*35*t^4*(1-t)^3 + p5y*21*t^5*(1-t)^2 + p6y*7*t^6*(1-t)^1 + p7y*t^7

s[t_] := (x'[t]*y''[t] - y'[t]*x''[t]) / (( x'[t]^2 + y'[t]^2 )^(3/2))

Print[s[t]]

pque = {
    p0x -> 0, p0y -> 0,
    p1x -> d, p1y -> 0,
    p2x -> d + d*Cos[a1], p2y -> d*Sin[a1],
    p3x -> d + d*Cos[a1] + d*Cos[a1+a2], p3y -> d*Sin[a1] + d*Sin[a1+a2],
    p4x -> p4xm, p4y -> p4ym,
    p5x -> (2*p4xm + p7xm)/3, p5y -> (2*p4ym + p7ym)/3,
    p6x -> (p4xm + 2*p7xm)/3, p6y -> (p4ym + 2*p7ym)/3,
    p7x -> p7xm, p7y -> p7ym
}

pram = {
    d -> 1, a1 -> 0.2, a2 -> 0.4,
    p4xm -> 2, p4ym -> -2, p7xm -> 5, p7ym -> 1
}

a1sol = Solve[(s[0] /. pque) == r0 && r0 <= 1 && -1 <= r0 && 0 <= d && a1 <= Pi /2 && -Pi / 2 <= a1, a1, Reals]

Print[a1sol]
