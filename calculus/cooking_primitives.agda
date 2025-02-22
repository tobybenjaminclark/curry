module cooking_primitives where

open import entity

postulate

  isEgg : Entity → Set
  isFlour : Entity → Set
  isBakingPowder : Entity → Set
  isMilk : Entity → Set
  isOatMilk : Entity → Set
  isCakeMix : Entity → Set
  isCakeBatter : Entity → Set

  OatMilkToMilk : ∀ (e : Entity) → isOatMilk e → isMilk e


  isBaked : Entity → Set
  Bake : ∀ (e : Entity) → isBaked e


record Egg : Set where
  constructor mkEgg
  field
    e₁            : Entity
    proofEgg      : isEgg e₁

record Flour : Set where
  constructor mkFlour
  field
    e₁            : Entity
    proofFlour      : isFlour e₁

record BakingPowder : Set where
  constructor mkBakingPowder
  field
    e₁            : Entity
    proofBakingPowder      : isBakingPowder e₁

record Milk : Set where
  constructor mkMilk
  field
    e₁            : Entity
    proofMilk      : isMilk e₁

record OatMilk : Set where
  constructor mkOatMilk
  field
    e₁            : Entity
    proofOatMilk      : isOatMilk e₁


record CakeBatter : Set where
  constructor mkCakeBatter
  field
    e1  :   Entity
    proofCakeBatter : isCakeBatter e1

record Cake : Set where
  constructor mkCake
  field
    e1  :   Entity
    
    ca1  :   isCakeMix e1
    ba1  :   isBaked e1

f : Milk → Flour → BakingPowder → Egg → Cake
f = {!   !}