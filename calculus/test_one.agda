module test_one where
    
open import Agda.Builtin.Equality
open import Data.Empty

postulate
  Entity         : Set
  isTomato       : Entity → Set
  isParsnip      : Entity → Set
  isCarrot       : Entity → Set
  isVegetable    : Entity → Set

  isChopped      : Entity → Set
  Chop           : ∀ (e : Entity) → isChopped e

  tomatoProofIsVegProof      : ∀ (e : Entity) → isTomato e → isVegetable e
  carrotProofIsVegProof      : ∀ (e : Entity) → isCarrot e → isVegetable e
  parsnipProofIsVegProof     : ∀ (e : Entity) → isParsnip e → isVegetable e

  _≠_ : Entity → Entity → Set

record Tomato : Set where
  constructor mkTomato
  field
    e₁           : Entity
    proofTomato  : isTomato e₁

record Parsnip : Set where
  constructor mkParsnip
  field
    e₁           : Entity
    proofParsnip : isParsnip e₁

record Vegetable : Set where
  constructor mkVegetable
  field
    e₁             : Entity
    proofVegetable : isVegetable e₁

record Salad : Set where
  constructor mkSalad
  field
    e₁  : Entity
    e₂  : Entity

    ve1 : isVegetable e₁
    ve2 : isVegetable e₂

    ch1 : isChopped e₁
    ch2 : isChopped e₂

    distinct : e₁ ≠ e₂

f : (e₁ : Tomato) → (e₂ : Parsnip) → Tomato.e₁ e₁ ≠ Parsnip.e₁ e₂ → Salad

f = {!   !}