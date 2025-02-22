open import Cubical.Core.Everything   
open import Cubical.Foundations.Prelude 
open import Cubical.Foundations.Isomorphism
open import Agda.Primitive

data Veg : Set where
  Tomato : Veg
  Potato : Veg
  Lettuce : Veg
  Carrot : Veg

data Salad : Set where
  mix : Veg → Veg → Salad

data ⊥ : Set where

-- a proof that two vegetables are distinct
-- this needs to be a universe so that the level of the types are the same.
¬_ : {ℓ : Level} → Set ℓ → Set ℓ
¬ A = A → ⊥

-- ensure two vegs are not the same
infix 1 _≢_
_≢_ : Veg → Veg → Set
x ≢ y = ¬ (x ≡ y)

-- constraint that v1 ≡/ v2
makeSalad : (v1 v2 : Veg) → v1 ≢ v2 → Salad
makeSalad v1 v2 _ = mix v1 v2

postulate
    tp : Tomato ≢ Potato

exSalad : Salad
exSalad = makeSalad Tomato Potato {! -m  !}

