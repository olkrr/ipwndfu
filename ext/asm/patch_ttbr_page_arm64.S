.text

.pool
.set TTBR0_BASE,            0xBAD00001
.set PAGE_OFFSET,           0xBAD00002
.set TLBI,                  0xBAD00003

; If you modify me, don't forget to change _inv_tlbi offset in patch_sigchecks

.globl _main
_main:
    MOV     X0, X30
    LDR     X1, =TTBR0_BASE
    LDR     X2, =PAGE_OFFSET
    LDR     X3, =TLBI
    LDR     X4, [X1, X2]
    MOV     X5, #0x6000000000000000
    BIC     X6, X4, X5
    CBZ     X6, #_else1
_bit62_61:
    ORR     X4, X4, X5, LSL #0
_else1:
    AND     X6, X4, #0x80
    CBZ     X6, #_patch
_bit7:
    EOR     X4, X4, #0x80
_patch:
    STR     X4, [X1, X2]
_sctlr:
    MRS     X4, SCTLR_EL1
    AND     X6, X4, #0x40000
    CBZ     X6, #_inv_tlbi
_bit19:
    EOR     X4, X4, #0x40000
    MSR     SCTLR_EL1, X4
_inv_tlbi:
    MOV     X0, X30
    ISB
    DMB     SY
    IC      IALLU
    TLBI    VMALLE1
    LDR     X3, =TLBI
    CBNZ    X3, #_alle3
    DSB     SY
    ISB
_ret:
    MOV     X30, X0
    RET
_alle3:
    TLBI    ALLE3
    DSB     SY
    ISB
    B       #_ret