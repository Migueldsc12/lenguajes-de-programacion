#!/bin/sh
# Este es un programa políglota para el Reto Extra.
# Funciona en: Bash, Python 3, Python 2, Ruby, y C (via gcc).
# El script detecta un intérprete o compilador y se re-ejecuta a sí mismo o compila una parte de sí mismo.

# --- INICIO: SCRIPT LOADER ---

# Intenta con Python 3
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$0" "$@"
fi

# Intenta con Python 2 
if command -v python >/dev/null 2>&1; then
    exec python "$0" "$@"
fi

# Intenta con Ruby
if command -v ruby >/dev/null 2>&1; then
    exec ruby "$0" "$@"
fi

#  Final: Compilar y ejecutar como C
if command -v gcc >/dev/null 2>&1; then

    awk '/^__C_CODE_BELOW__/ {f=1; next} f' "$0" > /tmp/maldad.c
    
    gcc /tmp/maldad.c -o /tmp/maldad_exec -lm
    
    /tmp/maldad_exec "$@"
    rm /tmp/maldad_exec /tmp/maldad.c
    exit $?
fi

echo "Error: No se encontró un intérprete (python3, python, ruby) ni compilador (gcc)." >&2
exit 1
# --- FIN: SCRIPT LOADER ---


# --- INICIO: CÓDIGO PYTHON ---
'''
=begin
'''

from __future__ import print_function
import math
import sys

def trib_py(k):
    if k <= 1: return 0
    if k == 2: return 1
    a, b, c = 0, 0, 1
    for _ in range(3, k + 1):
        a, b, c = b, c, a + b + c
    return c

if len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
        if n < 2:
            sys.exit(1)
        
        k = int(math.floor(math.log(n) / math.log(2)))
        
        print(trib_py(k + 2))
        sys.exit(0)
    except Exception:
        sys.exit(1)
'''
=end
'''
# --- FIN: CÓDIGO PYTHON ---


# --- INICIO: CÓDIGO RUBY ---

def trib_rb(k)
  return 0 if k <= 1
  return 1 if k == 2
  a, b, c = 0, 0, 1
  (3..k).each do
    a, b, c = b, c, a + b + c
  end
  return c
end

if ARGV.length > 0
  begin
    n = ARGV[0].to_i
    if n < 2
      exit 1
    end
    
    k = Math.log2(n).floor
    
    puts trib_rb(k + 2)
    exit 0 
  rescue
    exit 1
  end
end

# --- FIN: CÓDIGO RUBY ---


# --- INICIO: CÓDIGO C ---

__C_CODE_BELOW__
#include <stdio.h>
#include <stdlib.h>
#include <math.h> 

int trib_c(int k) {
    if (k <= 1) return 0;
    if (k == 2) return 1;
    
    int a = 0, b = 0, c = 1;
    for (int i = 3; i <= k; i++) {
        int next = a + b + c;
        a = b;
        b = c;
        c = next;
    }
    return c;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 1;
    }
    
    int n = atoi(argv[1]);
    if (n < 2) {
        return 1;
    }
    
    int k = (int)floor(log2((double)n));
    
    printf("%d\n", trib_c(k + 2));
    return 0;
}
# --- FIN: CÓDIGO C ---