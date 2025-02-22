
module test_one where
    
open import Agda.Builtin.Equality
open import Data.Empty




{- Entity : Set -}
postulate
  Entity         : Set
  isTomato       : Entity → Set
  isParsnip       : Entity → Set
  isCarrot       : Entity → Set
  isVegetable    : Entity → Set

  tomatoProofIsVegProof      : ∀ (e : Entity) → isTomato e → isVegetable e
  carrotProofIsVegProof      : ∀ (e : Entity) → isCarrot e → isVegetable e
  parsnipProofIsParsnipProof : ∀ (e : Entity) → isParsnip e → isVegetable e

  _≠_ : Entity → Entity → Set

record Tomato : Set where
  constructor mkTomato
  field
    e₁            : Entity
    proofTomato   : isTomato e₁

record Parsnip : Set where
  constructor mkParsnip
  field
    e₁            : Entity
    proofParsnip  : isParsnip e₁

record Vegetable : Set where
  constructor mkVegetable
  field
    e₁            : Entity
    proofVegeta   : isVegetable e₁


record Salad : Set where
    constructor mkSalad
    field
        e₁  :   Vegetable
        e₂  :   Vegetable
        distinct : Vegetable.e₁ e₁ ≠ Vegetable.e₁ e₂



f : (e₁ : Tomato) → (e₂ : Parsnip) → Tomato.e₁ e₁ ≠ Parsnip.e₁ e₂ → Salad
f = λ e₁ e₂ z →
    mkSalad
    (mkVegetable (Tomato.e₁ e₁)
     (tomatoProofIsVegProof (Tomato.e₁ e₁) (e₁ .Tomato.proofTomato)))
    (mkVegetable (Parsnip.e₁ e₂)
     (parsnipProofIsParsnipProof (Parsnip.e₁ e₂)
      (e₂ .Parsnip.proofParsnip)))
    z