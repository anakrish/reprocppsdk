import gdb
import os

segv = False

# Whenever execution stops, check if it was due to a SEGV.
def stop_handler (event):
    global segv
    if type(event) == gdb.SignalEvent:
        if event.stop_signal == "SIGSEGV":
            segv = True           
    if type(event) == gdb.BreakpointEvent:
        if "close" in gdb.selected_frame().name():
            print('\033[31m!!!!!!!!SOCKET CLOSED!!!!!!!!!!!!!!\033[0m')
            # Uncomment this to print callstack for socket close
            # gdb.execute('bt 30')
            pass
            
def repro():
    gdb.execute('set pagination off')
    gdb.execute('set breakpoint pending on')
    if not os.path.isdir('/app'): # myst execution
        gdb.execute('set substitute-path /usr appdir/usr')

    # Register stop handler
    gdb.events.stop.connect(stop_handler)

    # Set breakpoint in start_ops after descriptor_data check
    gdb.execute('b epoll_reactor.ipp:243')

    # Start execution
    gdb.execute('run')

    # Set breakpoint after socket close. Shows when sockets are closed.
    gdb.execute('b reactive_socket_service_base.ipp:113')

    # Each time the check is performed, control stops. Continue execution.
    # This results in other threads getting priority which might go on to
    # delete the descriptor before the thread that was stopped could use
    # the descriptor.
    for i in range(1, 150):
        if segv or not gdb.selected_inferior().threads():
            return
        gdb.execute('continue')

    print("Couldn't reproduce SEGV. Try tweaking loop ranges")
        
if __name__ == "__main__":
    repro()
