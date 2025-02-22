module cooking_primitives where

open import entity

postulate

  isEgg : Entity → Set
  isFlour : Entity → Set
  isCheese : Entity → Set
  isBakingPowder : Entity → Set
  isRiceFlour : Entity → Set
  isMilk : Entity → Set
  isOatMilk : Entity → Set

  RiceFlourToFlour : ∀ (e : Entity) → isRiceFlour e → isFlour e
  OatMilkToMilk : ∀ (e : Entity) → isOatMilk e → isMilk e

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

record Cheese : Set where
  constructor mkCheese
  field
    e₁            : Entity
    proofCheese      : isCheese e₁

record BakingPowder : Set where
  constructor mkBakingPowder
  field
    e₁            : Entity
    proofBakingPowder      : isBakingPowder e₁

record RiceFlour : Set where
  constructor mkRiceFlour
  field
    e₁            : Entity
    proofRiceFlour      : isRiceFlour e₁

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


record Cake : Set where
  constructor mkCake
  field
    e1  :   Entity
    e2  :   Entity
    e3  :   Entity
    e4  :   Entity

    p1  :   isFlour e1
    p2  :   isMilk e2
    p3  :   isEgg e3
    p4  :   isBakingPowder e4


f2 : OatMilk → Egg → Flour → BakingPowder → Cake
f2 = λ z z₁ z₂ z₃ →
    mkCake (z₂ .Flour.e₁) (z .OatMilk.e₁) (z₁ .Egg.e₁)
    (z₃ .BakingPowder.e₁) (z₂ .Flour.proofFlour)
    (OatMilkToMilk (z .OatMilk.e₁) (z .OatMilk.proofOatMilk))
    (z₁ .Egg.proofEgg) (z₃ .BakingPowder.proofBakingPowder)