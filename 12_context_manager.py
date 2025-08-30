# 12_context_manager.py — Context manager con __enter__/__exit__

class Temporizador:
    import time
    def __enter__(self):
        from time import perf_counter
        self.t0 = perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        from time import perf_counter
        self.dt = perf_counter() - self.t0
        print(f"Bloque tomó {self.dt:.6f} s")
        # devolver False para propagar excepciones si ocurrieron
        return False

if __name__ == "__main__":
    with Temporizador() as t:
        s = sum(range(2_000_00))
    print(f"Medido: {t.dt:.6f} s")
