# OpenCog AtomSpace Example: Grounding Extraction and Bounded Frontier

This example demonstrates the CairnPath AtomSpace adapter contract.

## Relation encoding

Use the traditional labeled-edge idiom:

```scheme
(EvaluationLink
  (PredicateNode "R")
  (ListLink FROM TO))
```

## Toy graph

```scheme
(use-modules (opencog) (opencog exec))

(define (C s) (ConceptNode s))
(define (Edge rel a b)
  (EvaluationLink (PredicateNode rel) (ListLink a b)))

(define A (C "A"))
(define B1 (C "B1"))
(define B2 (C "B2"))
(define C1 (C "C1"))
(define C2 (C "C2"))
(define C3 (C "C3"))

(Edge "R" A B1)
(Edge "R" A B2)
(Edge "R" B1 C1)
(Edge "R" B1 C2)
(Edge "R" B2 C2)
(Edge "R" B2 C3)
```

## One-hop MeetLink expansion

```scheme
(define (as-hop rel x)
  (let* ((q (MeetLink
              (VariableNode "$y")
              (EvaluationLink
                (PredicateNode rel)
                (ListLink x (VariableNode "$y")))))
         (v (cog-execute! q)))
    (cog-value->list v)))
```

Contract:

- `cog-execute!` executes the Atomese query.
- `cog-value->list` converts the returned Value container into a Scheme list.
- The adapter then normalizes each returned Atom to a CairnPath EntityRef.

## Dedup, rank, TopK

```scheme
(define (dedup-by-handle atoms)
  (let loop ((xs atoms) (seen '()) (out '()))
    (if (null? xs) (reverse out)
        (let* ((a (car xs))
               (h (cog-handle a)))
          (if (member h seen)
              (loop (cdr xs) seen out)
              (loop (cdr xs) (cons h seen) (cons a out)))))))

(define (rank-by-name atoms)
  (sort atoms (lambda (a b) (string<? (cog-name a) (cog-name b)))))

(define (topk atoms k)
  (let loop ((xs atoms) (i 0) (out '()))
    (if (or (null? xs) (>= i k)) (reverse out)
        (loop (cdr xs) (+ i 1) (cons (car xs) out)))))
```

## Bounded multi-hop traversal

```scheme
(define (expand-frontier rel frontier)
  (apply append (map (lambda (x) (as-hop rel x)) frontier)))

(define (cairnpath-traverse rel seed hops K)
  (let loop ((t 0) (frontier (list seed)))
    (if (>= t hops) frontier
        (let* ((cand  (expand-frontier rel frontier))
               (uniq  (dedup-by-handle cand))
               (ranked (rank-by-name uniq))
               (next  (topk ranked K)))
          (loop (+ t 1) next)))))

(cairnpath-traverse "R" A 2 10)
```

Expected semantic result:

- Hop 1 raw candidates: `B1`, `B2`.
- Hop 2 raw candidates: `C1`, `C2`, `C2`, `C3`.
- Hop 2 after dedup: `C1`, `C2`, `C3`.
- Final frontier count with `K=10`: 3.

## CairnPath StepTrace obligations

A compliant adapter must emit, per step:

- frontier count in,
- raw expanded count,
- deduplicated count,
- frontier count out,
- cap hit flag,
- frontier digest,
- backend query fingerprint,
- adapter version.
