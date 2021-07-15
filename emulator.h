#include <stdio.h>
#include <string>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <chrono>
#include <thread>
#include <cmath>
#include <cstdint>
#include <vector>
#include <set>
#include <SDL2/SDL.h>
#pragma once

// Set nth bit of target to value
#define BIT_SET(target, n, value) (target = (target & ~(1ULL << n)) | (value << n))
// check if nth bit of target is set
#define BIT_CHECK(target, n) ((target >> n) & 1ULL)

#define SCALE 4
#define WINDOW_WIDTH 128
#define FRAMERATE 60.0f

std::string getHex(char c);
std::string dumpMem(uint8_t *memory, unsigned size);

struct Operand {
    unsigned value;
    unsigned target;
    std::string type;
};

struct Registers {
    uint8_t R0 = 0;
    uint8_t R1 = 0;
    uint8_t R2 = 0;
    uint8_t R3 = 0;
    uint8_t R4 = 0;
    uint8_t R5 = 0;
    uint8_t R6 = 0;
    uint8_t R7 = 0;
    uint8_t S0 = 0b10000000;
    uint8_t S1 = 0;
    /*
        Flags in S0 (MSB to LSB)
        1   Hardwired 1
        0	Hardwired 0
        I   Interrupt Enable Flag	
        H	Halt
        -	
        N	Negative *not implemented
        Z	Zero
        C	Carry

        Flags in S1 (MSB to LSB)
        -
        -
        -
        -
        -
        -
        -
        -

    */
    unsigned short PC = 0;
    unsigned short SP = 0;
    unsigned short IX = 0;
    // CV, MD, MX
};

enum FlagRegister {
    S0,
    S1
};

enum InterruptType {
    ANY,
    KEYBOARD
};

class Bus;

class JalcoreCPU {
public:
    Registers registers;
    Bus *bus = nullptr;
    double cycle_total = 0;
    uint64_t cycle_counter = 0;

    JalcoreCPU();
    ~JalcoreCPU();

    void reset();

    void ConnectBus(Bus *b);
    void write(uint16_t addr, uint8_t data);
    uint8_t read(uint16_t addr);
    
    
    uint8_t read_byte();

    unsigned offset_address(uint8_t type, unsigned address);

    unsigned read_number(unsigned numBytes);
    unsigned read_number(uint16_t address, unsigned numBytes);

    bool is_2byte_register(uint8_t type);

    void get_types(unsigned amount, uint8_t* result);

    unsigned loadRegister(uint8_t type);

    void setRegister(uint8_t type, unsigned value);

    Operand get_aop(uint8_t type);

    void get_params(unsigned amount, Operand *result);

    void store(Operand operand, unsigned value);

    bool getFlag(FlagRegister target, unsigned bit);

    void setFlag(FlagRegister target, unsigned bit, bool value);

    // Instruction definitions
    void op_inc();
    void op_dec();
    void op_add();
    void op_addc();
    void op_sub();
    void op_subb();
    void op_rol();
    void op_rolc();
    void op_ror();
    void op_rorc();
    void op_and();
    void op_or();
    void op_xor();
    void op_cmp();
    void op_push();
    void op_pop();
    void op_jmp();
    void op_jsr();
    void op_mov();
    void op_ret();
    void op_rdw();

    void interrupt();

    void runtime_loop();

    void execute();

    std::vector<uint64_t> instruction_counts = std::vector<uint64_t>(0x16, 0);
    std::vector<double> instruction_times = std::vector<double>(0x16, 0.0f);
    uint16_t interrupt_address = 0x9FFE;
    uint16_t interrupt_type_address = 0x9FFD;
    bool interrupt_queued = false;
};

class JalcorePPU {
public:
    JalcorePPU();
    ~JalcorePPU();

    void ConnectBus(Bus* b);
    void Prepare();
    void SDL_eventloop();
    std::chrono::duration<double> UpdateDisplay();
    void Redraw();
    
    uint8_t *vram = nullptr;
    Bus *bus;

    SDL_Event event;
    SDL_Renderer *renderer;
    SDL_Window *window;
    SDL_Texture *texture;
    uint32_t pixels[WINDOW_WIDTH * WINDOW_WIDTH] = {};

    double redraw_total = 0;
    uint64_t redraw_count = 0;
    uint64_t vram_offset = 0xC000;

};

class Keyboard {
    // this is an IO device which handles interrupts for keyboard inputs
public:
    Keyboard();
    ~Keyboard();
    void ConnectBus(Bus *b);
    void handle_keypress(SDL_KeyboardEvent &event);

    Bus *bus;
    InterruptType interrupt_type = KEYBOARD;
    uint16_t keycode_type_address = 0x9FFB;
    uint16_t keycode_address = 0x9FFC;
    std::set<uint8_t> keys_pressed;
};

class Bus {
public:
    bool cpuRunning = false;
    bool guiRunning = false;
    
    Bus();
    ~Bus();

    void write(uint16_t addr, uint8_t data);
    uint8_t read(uint16_t addr);

    void loadRom(FILE* rom);

    void Startup();

    // Devices:
    std::thread cpu_thread;
    JalcoreCPU cpu;
    JalcorePPU ppu;
    Keyboard keyboard;
    const static uint64_t ramSize = 0x10000;
    uint8_t ram[ramSize] = {};
    
};