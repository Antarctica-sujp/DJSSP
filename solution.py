
import time
import random
from collections import defaultdict
import numpy as np
import copy
import multiprocessing


def process_generate_scratch(schedule_agent, cur_time, job_status, machine_status, coeff_tardiness, makespan_dict, data_ct_dict):
    makespan, op_seq_machines, job_seq_machines, start_time_op_macs, end_time_op_macs, start_time_ops, end_time_ops, mac_assignment_ops, flag_scheduled_ops, flag_scheduled_jobs = schedule_agent.generation_scratch(cur_time, job_status, machine_status, coeff_tardiness, 0)
    
    for ind_job_check in range(schedule_agent.num_job):
        name_job_check = schedule_agent.name_jobs[ind_job_check]
        type_job_check = schedule_agent.type_jobs[ind_job_check]
        priority_job_check = job_status[name_job_check]['priority']
            
        num_op_job_check = int( schedule_agent.num_op_jobs[ind_job_check] )
        idx_first_op_job_check = schedule_agent.idx_first_op_jobs[ind_job_check]
        for ind_op_job_check in range(num_op_job_check):
            op_check = int( idx_first_op_job_check + ind_op_job_check )
            
            if priority_job_check > 0:
                pending_constraint_op = schedule_agent.job_types[type_job_check][ind_op_job_check]['max_pend_time']
                
                time_comp = -1
                if ind_op_job_check == 0:
                    time_comp = schedule_agent.arrival_time_jobs[ind_job_check]
                    if time_comp < 0:
                        print('wrong arrival time')
                    # if time_comp <= 0:
                else: # not the first operation of this job
                    time_comp = end_time_ops[op_check - 1]
                #  if ind_op_job_check == 0:
                    
                if start_time_ops[op_check] - time_comp > pending_constraint_op:
                    print('violate the pending contraint')
                    makespan = makespan + 99999
                    # penalty_pending_constraint = penalty_pending_constraint + priority_job_check * 10 * (schedule_agent.start_time_ops[op_check] - time_comp - pending_constraint_op)
                # if end_time_ops[op_check] - time_comp >= pending_constraint_op:
            # if job_status[name_job_check]['priority'] > 0:
        # for ind_op_job_check in range(num_op_job_check):
    # for ind_job_check in range(self.num_job):
    
    makespan_dict[coeff_tardiness] = makespan
    data_ct_dict[coeff_tardiness] = [op_seq_machines, job_seq_machines, start_time_op_macs, end_time_op_macs, start_time_ops, end_time_ops, mac_assignment_ops, flag_scheduled_ops, flag_scheduled_jobs]
# def process_generate_scratch(schedule_agent, cur_time, job_status, machine_status, coeff_tardiness, makespan_dict):


def process_generate_resume(schedule_agent, cur_time, job_status, machine_status, coeff_tardiness, makespan_dict, data_ct_dict):
    makespan, new_op_seq_machines, new_job_seq_machines, new_start_time_op_macs, new_end_time_op_macs, new_start_time_ops, new_end_time_ops, new_mac_assignment_ops, new_flag_scheduled_ops, count_scheduled_op_macs, new_flag_scheduled_jobs = schedule_agent.generation_resume(cur_time, job_status, machine_status, coeff_tardiness, 0)
    
    for ind_job_check in range(schedule_agent.num_job):
        name_job_check = schedule_agent.name_jobs[ind_job_check]
        type_job_check = schedule_agent.type_jobs[ind_job_check]
        priority_job_check = job_status[name_job_check]['priority']
            
        num_op_job_check = int( schedule_agent.num_op_jobs[ind_job_check] )
        idx_first_op_job_check = schedule_agent.idx_first_op_jobs[ind_job_check]
        for ind_op_job_check in range(num_op_job_check):
            op_check = int( idx_first_op_job_check + ind_op_job_check )
            
            if priority_job_check > 0:
                pending_constraint_op = schedule_agent.job_types[type_job_check][ind_op_job_check]['max_pend_time']
                
                time_comp = -1
                if ind_op_job_check == 0:
                    time_comp = schedule_agent.arrival_time_jobs[ind_job_check]
                    if time_comp < 0:
                        print('wrong arrival time')
                    # if time_comp <= 0:
                else: # not the first operation of this job
                    time_comp = new_end_time_ops[op_check - 1]
                #  if ind_op_job_check == 0:
                    
                if new_start_time_ops[op_check] - time_comp > pending_constraint_op:
                    print('violate the pending contraint')
                    makespan = makespan + 99999
                    # penalty_pending_constraint = penalty_pending_constraint + priority_job_check * 10 * (schedule_agent.start_time_ops[op_check] - time_comp - pending_constraint_op)
                # if end_time_ops[op_check] - time_comp >= pending_constraint_op:
            # if job_status[name_job_check]['priority'] > 0:
        # for ind_op_job_check in range(num_op_job_check):
    # for ind_job_check in range(self.num_job):
        
    makespan_dict[coeff_tardiness] = makespan
    data_ct_dict[coeff_tardiness] = [new_op_seq_machines, new_job_seq_machines, new_start_time_op_macs, new_end_time_op_macs, new_start_time_ops, new_end_time_ops, new_mac_assignment_ops, new_flag_scheduled_ops, count_scheduled_op_macs, new_flag_scheduled_jobs]
# def process_generate_scratch(schedule_agent, cur_time, job_status, machine_status, coeff_tardiness, makespan_dict):
 
    
def process_iteration_scratch(schedule_agent, ind_process, cur_time, job_status, machine_status, coeff_tardiness, makespan_comp, makespan_dict, data_ct_dict):
    makespan_min = makespan_comp
    op_seq_machines_min = None
    job_seq_machines_min = None
    start_time_op_macs_min = None
    end_time_op_macs_min = None
    start_time_ops_min = None
    end_time_ops_min = None
    mac_assignment_ops_min = None
    flag_scheduled_ops_min = None
    flag_scheduled_jobs_min = None
    
    start_time_iter = time.time()
    elapsed_time_iter = 0
    while elapsed_time_iter < 12: # for ind_iter in range(7):
        makespan, op_seq_machines, job_seq_machines, start_time_op_macs, end_time_op_macs, start_time_ops, end_time_ops, mac_assignment_ops, flag_scheduled_ops, flag_scheduled_jobs = schedule_agent.generation_scratch(cur_time, job_status, machine_status, coeff_tardiness, 1)
        if makespan_min == -1 or makespan < makespan_min:
            for ind_job_check in range(schedule_agent.num_job):
                name_job_check = schedule_agent.name_jobs[ind_job_check]
                type_job_check = schedule_agent.type_jobs[ind_job_check]
                priority_job_check = job_status[name_job_check]['priority']
                # if schedule_agent.flag_scheduled_jobs[ind_job_check] != 1:
                #     print('unscheduled job')
                # # if flag_scheduled_jobs[flag_scheduled_jobs] != 0:
                    
                num_op_job_check = int( schedule_agent.num_op_jobs[ind_job_check] )
                idx_first_op_job_check = schedule_agent.idx_first_op_jobs[ind_job_check]
                for ind_op_job_check in range(num_op_job_check):
                    op_check = int( idx_first_op_job_check + ind_op_job_check )
                    # if self.flag_scheduled_ops[op_check] != 1:
                    #     print('unscheduled_ operation')
                    # # if flag_scheduled_ops[idx_first_op_job_check + ind_op_job_check] != 1:
                    
                    # if ind_op_job_check > 0:
                    #     if self.end_time_ops[op_check - 1] > self.start_time_ops[op_check]:
                    #         print('incorrect start time')
                    #     #  if end_time_ops[op_check - 1] > start_time_ops[op_check]:
                    # # if ind_op_job_check > 0:
                    
                    if priority_job_check > 0:
                        pending_constraint_op = schedule_agent.job_types[type_job_check][ind_op_job_check]['max_pend_time']
                        
                        time_comp = -1
                        if ind_op_job_check == 0:
                            time_comp = schedule_agent.arrival_time_jobs[ind_job_check]
                            if time_comp < 0:
                                print('wrong arrival time')
                            # if time_comp <= 0:
                        else: # not the first operation of this job
                            time_comp = end_time_ops[op_check - 1]
                        #  if ind_op_job_check == 0:
                            
                        if start_time_ops[op_check] - time_comp > pending_constraint_op:
                            print('violate the pending contraint')
                            makespan = makespan + 99999
                            # penalty_pending_constraint = penalty_pending_constraint + priority_job_check * 10 * (schedule_agent.start_time_ops[op_check] - time_comp - pending_constraint_op)
                        # if end_time_ops[op_check] - time_comp >= pending_constraint_op:
                    # if job_status[name_job_check]['priority'] > 0:
                # for ind_op_job_check in range(num_op_job_check):
            # for ind_job_check in range(self.num_job):
            
            if makespan < makespan_min:
                makespan_min = makespan
                op_seq_machines_min = copy.deepcopy(op_seq_machines)
                job_seq_machines_min = copy.deepcopy(job_seq_machines)
                start_time_op_macs_min = copy.deepcopy(start_time_op_macs)
                end_time_op_macs_min = copy.deepcopy(end_time_op_macs)
                start_time_ops_min = copy.deepcopy(start_time_ops)
                end_time_ops_min = copy.deepcopy(end_time_ops)
                mac_assignment_ops_min = copy.deepcopy(mac_assignment_ops)
                flag_scheduled_ops_min = copy.deepcopy(flag_scheduled_ops)
                flag_scheduled_jobs_min = copy.deepcopy(flag_scheduled_jobs)
            # makespan < makespan_min:
        # if makespan_min == -1 or makespan < makespan_min:
        elapsed_time_iter = time.time() - start_time_iter
    # while elapsed_time_iter < 14: 
        
    makespan_dict[ind_process] = makespan_min
    data_ct_dict[ind_process] = [op_seq_machines_min, job_seq_machines_min, start_time_op_macs_min, end_time_op_macs_min, start_time_ops_min, end_time_ops_min, mac_assignment_ops_min, flag_scheduled_ops_min, flag_scheduled_jobs_min]
# def process_iteration_scratch(schedule_agent, cur_time, job_status, machine_status, coeff_tardiness, makespan_dict, data_ct_dict):     

    
def process_iteration_resume(schedule_agent, ind_process, cur_time, job_status, machine_status, coeff_tardiness, makespan_comp, makespan_dict, data_dict):
    makespan_min = makespan_comp
    op_seq_machines_min = None
    job_seq_machines_min = None
    start_time_op_macs_min = None
    end_time_op_macs_min = None
    start_time_ops_min = None
    end_time_ops_min = None
    mac_assignment_ops_min = None
    flag_scheduled_ops_min = None
    count_scheduled_op_macs_min = None
    flag_scheduled_jobs_min = None
    
    start_time_iter = time.time()
    elapsed_time_iter = 0
    while elapsed_time_iter < 12: # for ind_iter in range(8):
        makespan, new_op_seq_machines, new_job_seq_machines, new_start_time_op_macs, new_end_time_op_macs, new_start_time_ops, new_end_time_ops, new_mac_assignment_ops, new_flag_scheduled_ops, count_scheduled_op_macs, new_flag_scheduled_jobs = schedule_agent.generation_resume(cur_time, job_status, machine_status, coeff_tardiness, 1)
        # makespan, op_seq_machines, job_seq_machines, start_time_op_macs, end_time_op_macs, start_time_ops, end_time_ops, mac_assignment_ops, flag_scheduled_ops, flag_scheduled_jobs = schedule_agent.generation_scratch(cur_time, job_status, machine_status, coeff_tardiness, 1)
        if makespan_min == -1 or makespan < makespan_min:
            for ind_job_check in range(schedule_agent.num_job):
                name_job_check = schedule_agent.name_jobs[ind_job_check]
                type_job_check = schedule_agent.type_jobs[ind_job_check]
                priority_job_check = job_status[name_job_check]['priority']
                # if schedule_agent.flag_scheduled_jobs[ind_job_check] != 1:
                #     print('unscheduled job')
                # # if flag_scheduled_jobs[flag_scheduled_jobs] != 0:
                    
                num_op_job_check = int( schedule_agent.num_op_jobs[ind_job_check] )
                idx_first_op_job_check = schedule_agent.idx_first_op_jobs[ind_job_check]
                for ind_op_job_check in range(num_op_job_check):
                    op_check = int( idx_first_op_job_check + ind_op_job_check )
                    # if self.flag_scheduled_ops[op_check] != 1:
                    #     print('unscheduled_ operation')
                    # # if flag_scheduled_ops[idx_first_op_job_check + ind_op_job_check] != 1:
                    
                    # if ind_op_job_check > 0:
                    #     if self.end_time_ops[op_check - 1] > self.start_time_ops[op_check]:
                    #         print('incorrect start time')
                    #     #  if end_time_ops[op_check - 1] > start_time_ops[op_check]:
                    # # if ind_op_job_check > 0:
                    
                    if priority_job_check > 0:
                        pending_constraint_op = schedule_agent.job_types[type_job_check][ind_op_job_check]['max_pend_time']
                        
                        time_comp = -1
                        if ind_op_job_check == 0:
                            time_comp = schedule_agent.arrival_time_jobs[ind_job_check]
                            if time_comp < 0:
                                print('wrong arrival time')
                            # if time_comp <= 0:
                        else: # not the first operation of this job
                            time_comp = new_end_time_ops[op_check - 1]
                        #  if ind_op_job_check == 0:
                            
                        if new_start_time_ops[op_check] - time_comp > pending_constraint_op:
                            print('violate the pending contraint')
                            makespan = makespan + 99999
                            # penalty_pending_constraint = penalty_pending_constraint + priority_job_check * 10 * (schedule_agent.start_time_ops[op_check] - time_comp - pending_constraint_op)
                        # if end_time_ops[op_check] - time_comp >= pending_constraint_op:
                    # if job_status[name_job_check]['priority'] > 0:
                # for ind_op_job_check in range(num_op_job_check):
            # for ind_job_check in range(self.num_job):
            
            if makespan < makespan_min:
                makespan_min = makespan
                op_seq_machines_min = copy.deepcopy(new_op_seq_machines)
                job_seq_machines_min = copy.deepcopy(new_job_seq_machines)
                start_time_op_macs_min = copy.deepcopy(new_start_time_op_macs)
                end_time_op_macs_min = copy.deepcopy(new_end_time_op_macs)
                start_time_ops_min = copy.deepcopy(new_start_time_ops)
                end_time_ops_min = copy.deepcopy(new_end_time_ops)
                mac_assignment_ops_min = copy.deepcopy(new_mac_assignment_ops)
                flag_scheduled_ops_min = copy.deepcopy(new_flag_scheduled_ops)
                count_scheduled_op_macs_min = copy.deepcopy(count_scheduled_op_macs)
                flag_scheduled_jobs_min = copy.deepcopy(new_flag_scheduled_jobs)
            # if makespan < makespan_min:
        # if makespan_min == -1 or makespan < makespan_min:
        elapsed_time_iter = time.time() - start_time_iter
    # while elapsed_time_iter < 13:
        
    makespan_dict[ind_process] = makespan_min
    data_dict[ind_process] = [op_seq_machines_min, job_seq_machines_min, start_time_op_macs_min, end_time_op_macs_min, start_time_ops_min, end_time_ops_min, mac_assignment_ops_min, flag_scheduled_ops_min, count_scheduled_op_macs_min, flag_scheduled_jobs_min]
# def process_iteration_scratch(schedule_agent, cur_time, job_status, machine_status, coeff_tardiness, makespan_dict, data_ct_dict):     



class Trainer:
    def __init__(self, Env, conf_list):
        self.conf_list = conf_list
        self.Env = Env
        self.checkpoint = None
        self.iter = 0
    # def __init__(self, Env, conf_list):

    def train(self, run_time):
        env = self.Env(self.conf_list[0])
        # obs = env.reset()
        machine_status, job_status, t, job_list = env.reset()
        return Agent(env.job_types, env.machines)
    # def train(self, run_time):
# class Trainer:

    
class Agent:
    def __init__(self, job_types, machines):
        self.machines = machines
        self.job_types = job_types
        self.total_num_ops = -1
        self.total_num_machines = 0
        self.perc_pend_time = 0.8
        self.set_coeff_tardiness = [1.0, 0.5, 0.2, 0.1, 0.05, 0.01]
        # coeff_tardiness = 0.5
        
        # num_cpu = multiprocessing.cpu_count()
        
        num_op_job_types = {} # np.zeros(num_job_type)
        key_dict_job_types = self.job_types.keys()
        num_job_types = len(key_dict_job_types)
        keys_job_types = []
        hash_ind_job_types = {}
        
        ind_job_type = 0
        for key_job_type in key_dict_job_types:
            keys_job_types.append(key_job_type)  
            num_op_temp = len(self.job_types[key_job_type])
            num_op_job_types[key_job_type] = num_op_temp
            hash_ind_job_types[key_job_type] = ind_job_type
            ind_job_type = ind_job_type + 1
        # for key_job_type in keys_job_type: 
        
        num_kind_mac = len(self.machines)
        num_machine_types = {} 
        hash_ind_mac_types = {}
        name_macs = []
        idx_mac_types = {}
        count_ind_mac = 0
        for machine_temp in self.machines:
            num_machine_types[machine_temp] = len(self.machines[machine_temp])
            idx_mac_types[machine_temp] = count_ind_mac
            # count_ind_mac = count_ind_mac + num_machine_types[machine_temp]
            self.total_num_machines = self.total_num_machines + num_machine_types[machine_temp]
            for ind_mac in range(num_machine_types[machine_temp]):
                mac_name_temp = self.machines[machine_temp][ind_mac]
                name_macs.append(mac_name_temp)
                hash_ind_mac_types[mac_name_temp] = ind_mac
                count_ind_mac = count_ind_mac + 1
            # for ind_mac in range(num_machine_types[machine_temp]):
        # for machine_temp in self.machines:
        
        keys_mac_types = []
        process_time_mac_jobs = {}      
        for machine_temp in self.machines:
            keys_mac_types.append(machine_temp)
            process_time_mac_jobs[machine_temp] = {}
            for key_job_type in key_dict_job_types:
                processing_time_temp = -1
                for ind_op_temp in range(num_op_job_types[key_job_type]):
                    if self.job_types[key_job_type][ind_op_temp]['machine_type'] == machine_temp:
                        processing_time_temp = self.job_types[key_job_type][ind_op_temp]['process_time']
                        break
                    # if self.job_types[key_job_type][ind_op_temp]['machine_type'] == machine_temp:                    
                # for ind_op_temp in range(num_op_job_types[key_job_type]):
                process_time_mac_jobs[machine_temp][key_job_type] = processing_time_temp
            # for key_job_type in key_dict_job_types:
        # for machine_temp in self.machines:
        
        
        max_num_comb_per_delta = 20
        threshold_num_iter = 5
        num_iter_expansion = 50
        delta_comb_macs = {}
        # comb_list_macs = {}
        # delta_list_macs = {}
        min_delta_macs = {}
        for machine_temp in self.machines:
            delta_comb_macs[machine_temp] = {}
            count_unique_delta = 0
            
            min_delta_temp = 0
            comb_list = []
            delta_list = []
            comb_ele = [0 for _ in range(num_job_types)]
            for ind_job_type in range(num_job_types):
                key_job_type = keys_job_types[ind_job_type]
                if process_time_mac_jobs[machine_temp][key_job_type] != -1:
                    comb_minus = comb_ele.copy()
                    comb_plus = comb_ele.copy()
                    comb_minus[ind_job_type] = 1
                    comb_list.append([comb_minus,comb_plus])
                    
                    delta_temp = -process_time_mac_jobs[machine_temp][key_job_type]
                    delta_list.append(delta_temp)
                    
                    if delta_temp not in delta_comb_macs[machine_temp]:
                        delta_comb_macs[machine_temp][delta_temp] = []
                        count_unique_delta = count_unique_delta + 1
                    # if delta_temp not in delta_comb_macs[machine_temp]:
                    if max_num_comb_per_delta > len(delta_comb_macs[machine_temp][delta_temp]):
                        delta_comb_macs[machine_temp][delta_temp].append([comb_minus,comb_plus])
                    # if max_num_comb_per_delta > len(delta_comb_macs[machine_temp][delta_temp]):
                    
                    if delta_temp < min_delta_temp:
                        min_delta_temp = delta_temp
                    # if delta_temp < min_delta_temp:
                # if process_time_mac_jobs[machine_temp][key_job_type] != -1:                
            # for key_job_type in key_dict_job_types:
            min_delta_macs[machine_temp] = min_delta_temp
            
            # comb_list_macs[machine_temp] = comb_list.copy()
            # delta_list_macs[machine_temp] = delta_list.copy()
            
            for ind_iter in range(num_iter_expansion):
                new_comb_list = []
                new_delta_list = []
                
                len_comb = len(comb_list)
                for ind_comb in range(len_comb):
                    delta_before = delta_list[ind_comb]
                    
                    for ind_job_type in range(num_job_types):
                        key_job_type = keys_job_types[ind_job_type]
                        processing_time_temp = process_time_mac_jobs[machine_temp][key_job_type]
                        
                        if processing_time_temp <= 0:
                            continue
                        # if processing_time_temp <= 0:
                        
                        comb_temp = copy.deepcopy(comb_list[ind_comb])
                        if comb_temp[1][ind_job_type] <= 0:
                            delta_new = delta_before - processing_time_temp
                            if delta_new < -min_delta_temp and delta_new >= min_delta_temp:
                                comb_temp[0][ind_job_type] = comb_temp[0][ind_job_type] + 1
                                if delta_new < 0 and delta_new not in delta_comb_macs[machine_temp]:
                                    delta_comb_macs[machine_temp][delta_new] = []
                                    count_unique_delta = count_unique_delta + 1
                                # if delta_temp not in delta_comb_macs[machine_temp]:
                                if delta_new < 0 and max_num_comb_per_delta > len(delta_comb_macs[machine_temp][delta_new]):
                                    flag_repetition = False
                                    for ind_comb_delta in range( len(delta_comb_macs[machine_temp][delta_new]) ):
                                        if delta_comb_macs[machine_temp][delta_new][ind_comb_delta] == comb_temp:
                                            flag_repetition = True
                                            break
                                        # if delta_comb_macs[machine_temp][delta_new][ind_comb_delta] == comb_temp:
                                    # for ind_comb_delta in range( len(delta_comb_macs[machine_temp][delta_new]) ):
                                    if flag_repetition == False:
                                        delta_comb_macs[machine_temp][delta_new].append(comb_temp)
                                    # if flag_repetition == False:
                                # if max_num_comb_per_delta > len(delta_comb_macs[machine_temp][delta_temp]):
                                
                                new_comb_list.append(comb_temp)
                                new_delta_list.append(delta_new)
                            # if delta_new < 0 and delta_new >= min_delta_temp:
                        # if comb_temp[1][ind_job_type] <= 0:
                            
                        comb_temp = copy.deepcopy(comb_list[ind_comb])
                        if comb_temp[0][ind_job_type] <= 0:
                            delta_new = delta_before + processing_time_temp
                            if delta_new < -min_delta_temp and delta_new >= min_delta_temp:
                                comb_temp[1][ind_job_type] = comb_temp[1][ind_job_type] + 1
                                if delta_new < 0 and delta_new not in delta_comb_macs[machine_temp]:
                                    delta_comb_macs[machine_temp][delta_new] = []
                                    count_unique_delta = count_unique_delta + 1
                                # if delta_temp not in delta_comb_macs[machine_temp]:
                                if delta_new < 0 and max_num_comb_per_delta > len(delta_comb_macs[machine_temp][delta_new]):
                                    flag_repetition = False
                                    for ind_comb_delta in range( len(delta_comb_macs[machine_temp][delta_new]) ):
                                        if delta_comb_macs[machine_temp][delta_new][ind_comb_delta] == comb_temp:
                                            flag_repetition = True
                                            break
                                        # if delta_comb_macs[machine_temp][delta_new][ind_comb_delta] == comb_temp:
                                    # for ind_comb_delta in range( len(delta_comb_macs[machine_temp][delta_new]) ):
                                    if flag_repetition == False:
                                        delta_comb_macs[machine_temp][delta_new].append(comb_temp)
                                    # if flag_repetition == False:
                                # if max_num_comb_per_delta > len(delta_comb_macs[machine_temp][delta_temp]):
                                
                                new_comb_list.append(comb_temp)
                                new_delta_list.append(delta_new)
                            # if delta_new < 0 and delta_new >= min_delta_temp: 
                        # if comb_temp[0][ind_job_type] <= 0:
                                
                    # for ind_job_type in range(num_job_types):
                    
                # for ind_comb in range(len_comb):
                comb_list = copy.deepcopy(new_comb_list)
                delta_list = copy.deepcopy(new_delta_list)
                
                if count_unique_delta + min_delta_temp >= 0 and ind_iter >= threshold_num_iter:
                    break
                # if count_unique_delta + min_delta_temp >= 0 and ind_iter >= 3:  
            # for ind_iter in range(10):
        # for machine_temp in self.machines:
        
        
        max_length_comb = 500
        num_iter_comb = 10
        length_comb_macs = {}
        for machine_type_temp in self.machines:
            length_comb_macs[machine_type_temp] = []
            list_base = [0]
            
            for count_iter in range(num_iter_comb):
                list_new = []
                for ind_list in range(len(list_base)):
                    for ind_job_type in range(num_job_types):
                        key_job_type = keys_job_types[ind_job_type]
                        if process_time_mac_jobs[machine_type_temp][key_job_type] != -1:
                            process_time_temp = process_time_mac_jobs[machine_type_temp][key_job_type]
                            length_temp = process_time_temp + list_base[ind_list]
                            if len(length_comb_macs[machine_type_temp] ) > 0:
                                pos_new = 0
                                sentinel_same = False
                                while pos_new < len(length_comb_macs[machine_type_temp] ):
                                    if length_comb_macs[machine_type_temp][pos_new] < length_temp:
                                        pos_new = pos_new + 1
                                    elif length_comb_macs[machine_type_temp][pos_new] == length_temp:
                                        sentinel_same = True
                                        break
                                    else:
                                        break
                                    # if length_comb_macs[machine_type_temp][pos_new] < process_time_temp:
                                # while pos_new < len(length_comb_macs[machine_type_temp] ):
                                if sentinel_same == False and max_length_comb > length_temp:
                                    length_comb_macs[machine_type_temp].insert(pos_new, length_temp)
                                    list_new.append(length_temp)
                                # if sentinel_same == False:
                            else:
                                length_comb_macs[machine_type_temp].append(process_time_temp + list_base[ind_list])
                                list_new.append(process_time_temp + list_base[ind_list])
                            # if len(length_comb_macs[machine_type_temp] ) > 0:
                        # if process_time_mac_jobs[machine_temp][key_job_type] != -1:
                    # for ind_job_type in range(num_job_types):
                # for ind_list in range(len(list_base)):
                list_base = list_new
            # for count_iter in range(num_iter_comb):
        # for machine_type_temp in self.machines:
        
        
        self.num_job_types = num_job_types
        self.num_kind_mac = num_kind_mac
        self.num_machine_types = num_machine_types
        self.idx_mac_types = idx_mac_types
        self.num_op_job_types = num_op_job_types
        self.key_dict_job_types = key_dict_job_types
        self.process_time_mac_jobs = process_time_mac_jobs
        self.delta_comb_macs = delta_comb_macs
        self.min_delta_macs = min_delta_macs
        self.keys_job_types = keys_job_types
        self.keys_mac_types = keys_mac_types
        self.hash_ind_mac_types = hash_ind_mac_types
        self.hash_ind_job_types = hash_ind_job_types
        self.name_macs = name_macs
        self.length_comb_macs = length_comb_macs
        self.max_length_comb = max_length_comb
        
        # self.sentinel_start = True        
    # def __init__(self, job_types, machines):


    def act(self, machine_status, job_status, cur_time, job_list):
        #----------------    Initialization    ----------------# 
        if cur_time == 0: # self.sentinel_start:
            self.init_construction(job_status, job_list, machine_status, cur_time)
        # if self.sentinel_start:
        
        
        #----------------   Breakdown Checking   ----------------# 
        sentinel_breakdown = False
        
        for machine_temp in machine_status:
            if self.flag_mac_available[machine_temp] == 1 and machine_status[machine_temp]['status'] == 'down':
                sentinel_breakdown = True
                self.mac_set_breakdown.append(machine_temp)
                self.flag_mac_available[machine_temp] = 0
                mac_type_breakdown = machine_status[machine_temp]['type']
                self.num_machine_available_types[mac_type_breakdown] = self.num_machine_available_types[mac_type_breakdown] - 1
            # if machine_status[machine_temp]['status'] == 'down':
        # for machine_temp in machine_status:
        
        
        #----------------   Restoration   ----------------#
        if sentinel_breakdown:  
            # coeff_tardiness = 0.5
            
            # start_time = time.time()
            
            manager = multiprocessing.Manager()
            makespan_ct_dict = manager.dict()
            data_ct_dict = manager.dict()
            
            jobs_ct = []
            # set_coeff_tardiness = [1.0, 0.5, 0.2, 0.1, 0.05, 0.01]
            for ind_process in range(6):
                proc = multiprocessing.Process(target=process_generate_resume, args=(self, cur_time, job_status, machine_status, self.set_coeff_tardiness[ind_process], makespan_ct_dict, data_ct_dict))
                jobs_ct.append(proc)
                proc.start()
            # for ind_process in range(6):
            for proc in jobs_ct:
                proc.join()
            # for proc in jobs:
            ct_min_makespan = min(makespan_ct_dict ,key = makespan_ct_dict.get)
            
            makespan_best = makespan_ct_dict[ct_min_makespan]
            new_op_seq_machines_best, new_job_seq_machines_best, new_start_time_op_macs_best, new_end_time_op_macs_best, new_start_time_ops_best, new_end_time_ops_best, new_mac_assignment_ops_best, new_flag_scheduled_ops_best, count_scheduled_op_macs_best, new_flag_scheduled_jobs_best = data_ct_dict[ct_min_makespan]
            
            if makespan_best > 9999:
                print(0)
            
            coeff_tardiness_best = ct_min_makespan
            
            #print(makespan_ct_dict.values())
            #print(ct_min_makespan)
            #print(makespan_ct_dict[ct_min_makespan])
            
            makespan_rnd_dict = manager.dict()
            data_rnd_dict = manager.dict() 
            jobs_rnd = []
            for ind_process in range(6):
                proc = multiprocessing.Process(target=process_iteration_resume, args=(self, ind_process, cur_time, job_status, machine_status, coeff_tardiness_best, makespan_best, makespan_rnd_dict, data_rnd_dict))
                jobs_rnd.append(proc)
                proc.start()
            # for ind_process in range(6):
            for proc in jobs_rnd:
                proc.join()
            # for proc in jobs:
            ind_rnd_min_makespan = min(makespan_rnd_dict ,key = makespan_rnd_dict.get)
            if makespan_rnd_dict[ind_rnd_min_makespan] < makespan_best:
                makespan_best = makespan_rnd_dict[ind_rnd_min_makespan]
                new_op_seq_machines_best, new_job_seq_machines_best, new_start_time_op_macs_best, new_end_time_op_macs_best, new_start_time_ops_best, new_end_time_ops_best, new_mac_assignment_ops_best, new_flag_scheduled_ops_best, count_scheduled_op_macs_best, new_flag_scheduled_jobs_best  = data_rnd_dict[ind_rnd_min_makespan]
            # if makespan_rnd_dict[ind_rnd_min_makespan] < makespan_best:
            
            # elapsed_time = (time.time() - start_time)
            # print(elapsed_time)
            
            # makespan, new_op_seq_machines, new_job_seq_machines, new_start_time_op_macs, new_end_time_op_macs, new_start_time_ops, new_end_time_ops, new_mac_assignment_ops, new_flag_scheduled_ops, count_scheduled_op_macs, new_flag_scheduled_jobs = self.generation_resume(cur_time, job_status, machine_status, coeff_tardiness)
            
            self.op_seq_machines = new_op_seq_machines_best
            self.job_seq_machines = new_job_seq_machines_best
            self.start_time_op_macs = new_start_time_op_macs_best
            self.end_time_op_macs = new_end_time_op_macs_best
            self.start_time_ops = new_start_time_ops_best
            self.end_time_ops = new_end_time_ops_best
            self.mac_assignment_ops = new_mac_assignment_ops_best
            self.flag_scheduled_ops = new_flag_scheduled_ops_best
            self.count_scheduled_op_macs = count_scheduled_op_macs_best
            self.new_flag_scheduled_jobs = new_flag_scheduled_jobs_best
            
            
            #----------------   Verification   ----------------#
            penalty_pending_constraint = 0
            for ind_job_check in range(self.num_job):
                name_job_check = self.name_jobs[ind_job_check]
                type_job_check = self.type_jobs[ind_job_check]
                priority_job_check = job_status[name_job_check]['priority']
                if self.flag_scheduled_jobs[ind_job_check] != 1:
                    print('unscheduled job')
                # if flag_scheduled_jobs[flag_scheduled_jobs] != 0:
                    
                num_op_job_check = int( self.num_op_jobs[ind_job_check] )
                idx_first_op_job_check = self.idx_first_op_jobs[ind_job_check]
                for ind_op_job_check in range(num_op_job_check):
                    op_check = int( idx_first_op_job_check + ind_op_job_check )
                    if self.flag_scheduled_ops[op_check] != 1:
                        print('unscheduled_ operation')
                    # if flag_scheduled_ops[idx_first_op_job_check + ind_op_job_check] != 1:
                    
                    if ind_op_job_check > 0:
                        if self.end_time_ops[op_check - 1] > self.start_time_ops[op_check]:
                            print('incorrect start time')
                        #  if end_time_ops[op_check - 1] > start_time_ops[op_check]:
                    # if ind_op_job_check > 0:
                    
                    if priority_job_check > 0:
                        pending_constraint_op = self.job_types[type_job_check][ind_op_job_check]['max_pend_time']
                        
                        time_comp = -1
                        if ind_op_job_check == 0:
                            time_comp = self.arrival_time_jobs[ind_job_check]
                            if time_comp < 0:
                                print('wrong arrival time')
                            # if time_comp <= 0:
                        else: # not the first operation of this job
                            time_comp = self.end_time_ops[op_check - 1]
                        #  if ind_op_job_check == 0:
                            
                        if self.start_time_ops[op_check] - time_comp > pending_constraint_op:
                            print('violate the pending contraint')
                            penalty_pending_constraint = penalty_pending_constraint + priority_job_check * 10 * (self.start_time_ops[op_check] - time_comp - pending_constraint_op)
                        # if end_time_ops[op_check] - time_comp >= pending_constraint_op:
                    # if job_status[name_job_check]['priority'] > 0:
                # for ind_op_job_check in range(num_op_job_check):
            # for ind_job_check in range(self.num_job):
            for machine_temp in machine_status:
                len_op_seq = len(self.op_seq_machines[machine_temp])
                for ind_op_seq in range(len_op_seq-1):
                    if self.end_time_op_macs[machine_temp][ind_op_seq] > self.start_time_op_macs[machine_temp][ind_op_seq+1]:
                        print('Incorrect start time')
                    # if new_end_time_op_macs[machine_temp][ind_op_seq] > new_start_time_op_macs[machine_temp][ind_op_seq+1]:
                # for ind_op_seq in range(len_op_seq-1):
            # for machine_temp in machine_status:
            
            print(penalty_pending_constraint)
        # if sentinel_breakdown:  
        
        action = {}
        for machine_temp in job_list:
            ind_job_schedule_mac = self.count_scheduled_op_macs[machine_temp]
            if ind_job_schedule_mac >= len(self.start_time_op_macs[machine_temp]):
                continue
            # if ind_job_schedule_mac >= len(self.start_time_op_macs[machine_temp]):
            if cur_time == self.start_time_op_macs[machine_temp][ind_job_schedule_mac]:
                action[machine_temp] = self.job_seq_machines[machine_temp][ind_job_schedule_mac]
                self.count_scheduled_op_macs[machine_temp] = self.count_scheduled_op_macs[machine_temp] + 1
            # if cur_time == self.start_time_op_macs[machine_temp][ind_job_schedule_mac]:
        # for machine_temp in job_list:
        
        return action 
    # def act(self, machine_status, job_status, cur_time, job_list):
    
        
    def generation_resume(self, cur_time, job_status, machine_status, coeff_tardiness, rnd_mode):
        count_scheduled_op_macs = {}
        for machine_temp in self.name_macs:
            count_scheduled_op_macs[machine_temp] = 0
        # for machine_temp in key_job_list:
        
        
        #----------------   Construction   ----------------#
        big_num = 99999
        # new_num_job_dispatch_mac = self.group_job_mac.copy()
        new_op_seq_machines = {}
        new_job_seq_machines = {}
        new_start_time_op_macs = {}
        new_end_time_op_macs = {}
        new_op_anchor_type_macs = {}
        for machine_temp in machine_status:
            new_op_seq_machines[machine_temp] = []
            new_job_seq_machines[machine_temp] = []
            new_start_time_op_macs[machine_temp] = []
            new_end_time_op_macs[machine_temp] = []
            new_op_anchor_type_macs[machine_temp] = -1
        # for machine_temp in self.machines:
        new_flag_scheduled_jobs = np.zeros(self.num_job)
        new_flag_scheduled_ops = np.zeros(self.total_num_ops)
        new_start_time_ops = -1 * np.ones(self.total_num_ops)
        new_end_time_ops = -1 * np.ones(self.total_num_ops)
        
        new_mac_assignment_ops = {}
        new_ready_time_type_macs = {}
        flag_available_type_macs= {}
        available_mac_offset = {}
        # broken_mac_offset = {}
        new_scheduled_length_mac_types = {}
        for machine_type_temp in self.machines:
            new_ready_time_type_macs[machine_type_temp] = np.zeros(self.num_machine_types[machine_type_temp]) # [0 for _ in range(self.num_machine_types[machine_type_temp])]
            flag_available_type_macs[machine_type_temp] = np.ones(self.num_machine_types[machine_type_temp]) 
            available_mac_offset[machine_type_temp] = np.zeros(self.num_machine_types[machine_type_temp])
            # broken_mac_offset[machine_type_temp] = np.zeros(self.num_machine_types[machine_type_temp])
            new_scheduled_length_mac_types[machine_type_temp] = 0
        # for machine_type_temp in self.machines:
        for ind_mac_broken in range(len(self.mac_set_breakdown)):
            mac_broken = self.mac_set_breakdown[ind_mac_broken]
            type_mac_broken = machine_status[mac_broken]['type']
            hash_idx_mac_broken = self.hash_ind_mac_types[mac_broken]
            flag_available_type_macs[type_mac_broken][hash_idx_mac_broken] = 0
            available_mac_offset[type_mac_broken][hash_idx_mac_broken] = big_num
            # broken_mac_offset[type_mac_broken][hash_idx_mac_broken] = -big_num
        # for ind_mac_broken in range(len(mac_set_breakdown)):
        
        num_scheduled_jobs_per_type = {}
        for key_job_type in self.key_dict_job_types:
            num_scheduled_jobs_per_type[key_job_type] = 0
        # for key_job_type in self.key_dict_job_types:
        
        occupy_time_type_macs = {}
        cumul_pend_time_type_macs = {}
        for mac_type_temp in self.machines:
            occupy_time_type_macs[mac_type_temp] = np.zeros(self.num_machine_types[mac_type_temp])
            cumul_pend_time_type_macs[mac_type_temp] = np.zeros(self.num_machine_types[mac_type_temp])
        # for mac_type_temp in self.machines:    
        
        
        #----------------   Retention   ----------------#
        ordinary_job_inspect_list = []
        
        for machine_temp in self.name_macs:
            mac_type_temp = machine_status[machine_temp]['type']
            hash_ind_mac_temp = self.hash_ind_mac_types[machine_temp]
            ind_op_mac_temp = 0
            len_op_mac_temp = len(self.op_seq_machines[machine_temp])
            while ind_op_mac_temp < len_op_mac_temp:   
                idx_op_temp = self.op_seq_machines[machine_temp][ind_op_mac_temp]
                ind_job_op_temp = self.ind_job_ops[idx_op_temp]  # self.job_seq_machines[machine_temp][ind_op_mac_temp]
                job_name_temp = self.name_jobs[ind_job_op_temp]
                ind_op_op_temp = self.ind_op_ops[idx_op_temp]
                job_type_temp = self.type_jobs[ind_job_op_temp]
                priority_job_temp = job_status[job_name_temp]['priority']
                
                if self.start_time_op_macs[machine_temp][ind_op_mac_temp] >= cur_time:
                    break
                # if self.start_time_op_macs[machine_temp][ind_op_mac_temp] >= cur_time:
                
                if self.flag_mac_available[machine_temp] == 0 and self.end_time_op_macs[machine_temp][ind_op_mac_temp] > cur_time:   
                    break
                # if self.flag_mac_available[machine_temp] == 0 and self.end_time_op_macs[machine_temp][ind_op_mac_temp] > cur_time:   
                
                new_op_seq_machines[machine_temp].append(idx_op_temp)
                new_job_seq_machines[machine_temp].append(job_name_temp)
                new_start_time_op_macs[machine_temp].append(self.start_time_op_macs[machine_temp][ind_op_mac_temp])
                new_end_time_op_macs[machine_temp].append(self.end_time_op_macs[machine_temp][ind_op_mac_temp])
                new_start_time_ops[idx_op_temp] = self.start_time_ops[idx_op_temp]
                new_end_time_ops[idx_op_temp] = self.end_time_ops[idx_op_temp]
                process_time_temp = new_end_time_ops[idx_op_temp] - new_start_time_ops[idx_op_temp] # self.job_types[job_type_temp][ind_op_op_temp]['process_time']
                new_scheduled_length_mac_types[mac_type_temp] = new_scheduled_length_mac_types[mac_type_temp] + process_time_temp
                new_flag_scheduled_ops[idx_op_temp] = 1
                new_mac_assignment_ops[idx_op_temp] = machine_temp
                
                occupy_time_type_macs[mac_type_temp][hash_ind_mac_temp] = occupy_time_type_macs[mac_type_temp][hash_ind_mac_temp] + process_time_temp
                
                # if self.priority_jobs[ind_job_op_temp] <= 0:
                #     new_op_anchor_type_macs[machine_temp] = idx_op_temp    
                # # if self.priority_jobs[ind_job_op_temp] <= 0:
                
                if ind_op_op_temp == 0:
                    new_flag_scheduled_jobs[ind_job_op_temp] = 1
                    # new_count_scheduled_jobs = new_count_scheduled_jobs + 1  
                    if priority_job_temp <= 0:
                        ordinary_job_inspect_list.append(ind_job_op_temp)
                        num_scheduled_jobs_per_type[job_type_temp] = num_scheduled_jobs_per_type[job_type_temp] + 1
                    # if priority_job_temp > 0:                                         
                # if ind_op_op_temp == 0:
                    
                if ind_op_mac_temp > 0:
                    pend_time_temp = new_start_time_ops[ind_op_mac_temp] - new_end_time_ops[ind_op_mac_temp-1]
                    if pend_time_temp > 0:
                        cumul_pend_time_type_macs[mac_type_temp][hash_ind_mac_temp] = cumul_pend_time_type_macs[mac_type_temp][hash_ind_mac_temp] + pend_time_temp
                    # if pend_time_temp > 0:
                # if ind_op_mac_temp > 0:
                
                count_scheduled_op_macs[machine_temp] = count_scheduled_op_macs[machine_temp] + 1
                
                ind_op_mac_temp = ind_op_mac_temp + 1
            # while ind_op_mac_temp < len_op_mac_temp:   
            
            
            if len(new_end_time_op_macs[machine_temp]) > 0:
                new_ready_time_type_macs[mac_type_temp][hash_ind_mac_temp] = new_end_time_op_macs[machine_temp][-1] # self.end_time_op_macs[machine_temp][ind_op_mac_temp]
                if new_ready_time_type_macs[mac_type_temp][hash_ind_mac_temp] < cur_time:
                    new_ready_time_type_macs[mac_type_temp][hash_ind_mac_temp] = cur_time
                # if new_ready_time_type_macs[mac_type_temp][hash_ind_mac_temp] < cur_time:
            # if len(new_end_time_op_macs[machine_temp]) > 0: 
            
        # for machine_temp in self.name_macs:
            
            
        #----------------   Priority   ----------------#
        for ind_set_job_priority in range(self.size_set_job_priority):
            name_job_priority = self.set_job_priority[ind_set_job_priority]
            idx_job_priority = int( self.idx_set_job_priority[name_job_priority] )
            type_job_priority = self.type_jobs[idx_job_priority]
            num_op_job_priority = int( self.num_op_jobs[idx_job_priority] )
            idx_first_op_job_priority = self.idx_first_op_jobs[idx_job_priority]
            
            job_constraint_temp = self.arrival_jobs_priority[name_job_priority]
            for ind_op_job_priority in range(num_op_job_priority):
                idx_op_schedule = int( idx_first_op_job_priority + ind_op_job_priority )
                if new_flag_scheduled_ops[idx_op_schedule] == 1:
                    if new_end_time_ops[idx_op_schedule] > job_constraint_temp:
                        job_constraint_temp = new_end_time_ops[idx_op_schedule] 
                    # if new_end_time_ops[idx_op_schedule] > job_constraint_temp:
                    continue
                # if new_flag_scheduled_ops[idx_op_schedule] == 1:
                
                mac_type_op_schedule = self.machine_type_ops[idx_op_schedule]
                process_time_op_schedule = self.process_time_mac_jobs[mac_type_op_schedule][type_job_priority]
                pend_time_op_schedule = self.job_types[type_job_priority][ind_op_job_priority]['max_pend_time']
                
                start_time_final = -1
                pend_time_final = -1
                mac_op_final = None
                ind_position_final = -1
                
                num_mac_same_type = self.num_machine_types[mac_type_op_schedule]
                idx_mac_min_leng = np.argmin(occupy_time_type_macs[mac_type_op_schedule] + cumul_pend_time_type_macs[mac_type_op_schedule] + available_mac_offset[mac_type_op_schedule])
                if rnd_mode == 1:
                    idx_mac_min_leng = random.randint(0, num_mac_same_type-1)
                    mac_min_leng = self.machines[mac_type_op_schedule][idx_mac_min_leng]
                    while self.flag_mac_available[mac_min_leng] == 0:
                        idx_mac_min_leng = random.randint(0, num_mac_same_type-1)
                        mac_min_leng = self.machines[mac_type_op_schedule][idx_mac_min_leng]
                    # while self.flag_mac_available[mac_op_schedule] == 0:
                # if rnd_mode == 1:
                
                #-----------   Postpone   -----------#
                # if pend_time_final > 0:
                count_attempt = 0
                idx_mac_op_schedule = idx_mac_min_leng
                while count_attempt < num_mac_same_type:
                    mac_op_schedule = self.machines[mac_type_op_schedule][idx_mac_op_schedule]
                    if self.flag_mac_available[mac_op_schedule] == 0:
                        idx_mac_op_schedule = (idx_mac_op_schedule + 1) % num_mac_same_type
                        count_attempt = count_attempt + 1
                        continue
                    # if self.flag_mac_available[mac_candidate] == 0:
                    
                    start_time_candidate = job_constraint_temp
                    if len(new_end_time_op_macs[mac_op_schedule]) > 0:
                        if new_end_time_op_macs[mac_op_schedule][-1] > start_time_candidate:
                            start_time_candidate = new_end_time_op_macs[mac_op_schedule][-1]
                        # if new_end_time_op_macs[mac_op_schedule][-1] > start_time_candidate:
                    # if len(new_end_time_op_macs[mac_op_schedule]) > 0:
                    if start_time_candidate < cur_time:
                        start_time_candidate = cur_time
                    # if start_time_candidate < cur_time:
                    
                    if job_constraint_temp + pend_time_op_schedule - start_time_candidate < 0:
                        sentinel_feasible, start_time_ops_trial, end_time_ops_trial, start_time_op_macs_trial, end_time_op_macs_trial = self.priority_backward(cur_time, new_start_time_ops, new_end_time_ops, new_start_time_op_macs, new_end_time_op_macs, ind_op_job_priority, start_time_candidate, pend_time_op_schedule, idx_first_op_job_priority, idx_job_priority, new_mac_assignment_ops, new_op_seq_machines)
                        if sentinel_feasible:
                            pend_time_final = 0
                            mac_op_final = mac_op_schedule
                            start_time_final = start_time_candidate
                            ind_position_final = len(new_op_seq_machines[mac_op_final])
                            new_start_time_ops = start_time_ops_trial # copy.deepcopy(start_time_ops)
                            new_end_time_ops = end_time_ops_trial # copy.deepcopy(end_time_ops)
                            new_start_time_op_macs = start_time_op_macs_trial # copy.deepcopy(start_time_op_macs)
                            new_end_time_op_macs = end_time_op_macs_trial # copy.deepcopy(end_time_op_macs)
                            break
                        # sentinel_feasible
                    else:
                        pend_time_final = 0
                        mac_op_final = mac_op_schedule
                        start_time_final = start_time_candidate
                        ind_position_final = len(new_op_seq_machines[mac_op_final])
                    # if job_constraint_temp + pend_time_op_schedule - start_time_candidate < 0:  
                    idx_mac_op_schedule = (idx_mac_op_schedule + 1) % num_mac_same_type
                    count_attempt = count_attempt + 1
                # while count_attempt < num_mac_same_type:
                # if pend_time_final > 0:
                
                
                
                #-----------   Last Insertion   -----------#
                if pend_time_final == -1:
                    count_attempt = 0
                    idx_mac_op_schedule = idx_mac_min_leng
                    while count_attempt < num_mac_same_type:
                        mac_candidate = self.machines[mac_type_op_schedule][idx_mac_op_schedule]
                        if self.flag_mac_available[mac_candidate] == 0:
                            idx_mac_op_schedule = (idx_mac_op_schedule + 1) % num_mac_same_type
                            count_attempt = count_attempt + 1
                            continue
                        # if self.flag_mac_available[mac_candidate] == 0:
                        
                        start_time_candidate = job_constraint_temp
                        if len(new_end_time_op_macs[mac_candidate]) > 0:
                            if new_end_time_op_macs[mac_candidate][-1] > start_time_candidate:
                                start_time_candidate = new_end_time_op_macs[mac_candidate][-1]
                            # if new_end_time_op_macs[mac_candidate][-1] > start_time_candidate:
                        # if len(new_end_time_op_macs[mac_candidate]) > 0:
                        if start_time_candidate < cur_time:
                            start_time_candidate = cur_time
                        # if start_time_candidate < cur_time:
                        
                        pend_time_candidate = start_time_candidate - job_constraint_temp - pend_time_op_schedule
                        if pend_time_final == -1:
                            pend_time_final = pend_time_candidate
                            mac_op_final = mac_candidate
                            start_time_final = start_time_candidate
                            ind_position_final = len(new_op_seq_machines[mac_op_final])
                        elif pend_time_candidate < pend_time_final:
                            pend_time_final = pend_time_candidate
                            mac_op_final = mac_candidate
                            start_time_final = start_time_candidate
                            ind_position_final = len(new_op_seq_machines[mac_op_final])
                        # if pend_time_final == -1:
                        
                        if pend_time_final <= 0:
                            break
                        # if pend_time_candidate <= 0:
                        
                        idx_mac_op_schedule = (idx_mac_op_schedule + 1) % num_mac_same_type
                        count_attempt = count_attempt + 1
                    # while count_attempt < num_mac_same_type:
                # if pend_time_final > 0:
                
                
                #-------    update intermediate data    -------#
                new_start_time_ops[idx_op_schedule] = start_time_final
                new_end_time_ops[idx_op_schedule] = start_time_final + process_time_op_schedule
                new_op_seq_machines[mac_op_final].insert(ind_position_final, idx_op_schedule)
                new_job_seq_machines[mac_op_final].insert(ind_position_final, name_job_priority)
                new_start_time_op_macs[mac_op_final].insert(ind_position_final, new_start_time_ops[idx_op_schedule])
                new_end_time_op_macs[mac_op_final].insert(ind_position_final, new_end_time_ops[idx_op_schedule])
                new_mac_assignment_ops[idx_op_schedule] = mac_op_final
                new_flag_scheduled_ops[idx_op_schedule] = 1
                new_scheduled_length_mac_types[mac_type_op_schedule] = new_scheduled_length_mac_types[mac_type_op_schedule] + process_time_op_schedule
                occupy_time_type_macs[mac_type_op_schedule][idx_mac_op_schedule] = occupy_time_type_macs[mac_type_op_schedule][idx_mac_op_schedule] + process_time_op_schedule
                
                job_constraint_temp = new_end_time_ops[idx_op_schedule] 
            # for ind_op_job_priority in range(num_op_job_priority):
            new_flag_scheduled_jobs[idx_job_priority] = 1
        # for ind_job_priority in range(size_set_job_priority):
        
            
        #----------------   Unfinished Jobs   ----------------#
        pos_insertion_macs = {}
        op_priority_ref_macs = {}
        for mac_type_temp in self.machines:
            num_mac_type_temp = self.num_machine_types[mac_type_temp]
            # pos_insertion_type_mac[mac_type_temp] = np.zeros(num_mac_type_temp)
            for ind_mac_type in range(num_mac_type_temp):
                mac_name_temp = self.machines[mac_type_temp][ind_mac_type]
                count_scheduled_op_temp = count_scheduled_op_macs[mac_name_temp]
                pos_insertion_macs[mac_name_temp] = count_scheduled_op_temp
                if count_scheduled_op_temp < len(new_op_seq_machines[mac_name_temp]):
                    op_temp = new_op_seq_machines[mac_name_temp][count_scheduled_op_temp]
                    ind_job_temp = self.ind_job_ops[op_temp]
                    name_job_temp = self.name_jobs[ind_job_temp]
                    priority_job_temp = self.priority_jobs_priority[name_job_temp]
                    if priority_job_temp > 0:
                        op_priority_ref_macs[mac_name_temp] = int( op_temp )
                    else:
                        print('incorrect processing sequence')
                    # if priority_job_temp > 0:
                else:
                    op_priority_ref_macs[mac_name_temp] = -1
                # pos_insertion_macs[mac_name_temp] = count_scheduled_op_temp
                
            # for ind_mac_type in range(num_mac_type_temp):
        # for mac_type_temp in self.machines:
        
        for machine_temp in machine_status:
            num_op_mac_temp = len(new_op_seq_machines[machine_temp])
            # ind_last_ordinary_op = 0
            for ind_op_mac in range(num_op_mac_temp):
                op_iter = new_op_seq_machines[machine_temp][ind_op_mac]
                ind_job_op_iter = self.ind_job_ops[op_iter]
                priority_op_iter = self.priority_jobs[ind_job_op_iter]
                if priority_op_iter == 0:
                    new_op_anchor_type_macs[machine_temp] = op_iter
                # if priority_op_iter == 0:
            # for ind_op_mac in range(num_op_mac_temp):
        # for machine_temp in machine_status:    
        
        
        set_job_unfinished = []
        idx_op_set_job_unfinished = [] 
        final_idx_op_set_job_unfinished = []
        job_constraint_set_job_unfinished = []
        for job_inspect in ordinary_job_inspect_list:
            idx_first_op_job_inspect = int( self.idx_first_op_jobs[job_inspect] )
            num_op_job_inspect = int( self.num_op_jobs[job_inspect] )
            for ind_op_iter_inspect in range(num_op_job_inspect):
                if new_flag_scheduled_ops[int( idx_first_op_job_inspect + ind_op_iter_inspect)] != 1:
                    set_job_unfinished.append(job_inspect)
                    idx_op_set_job_unfinished.append(idx_first_op_job_inspect + ind_op_iter_inspect)
                    final_idx_op_set_job_unfinished.append(idx_first_op_job_inspect + num_op_job_inspect - 1)
                    end_time_op_prev = new_end_time_ops[int(idx_first_op_job_inspect + ind_op_iter_inspect - 1)] 
                    if ind_op_iter_inspect != 0 and end_time_op_prev > 0:
                        job_constraint_set_job_unfinished.append(end_time_op_prev)
                    # if ind_op_iter_inspect != 0 and end_time_op_prev > 0:
                    break
                # if new_flag_scheduled_ops[idx_first_op_job_inspect + ind_op_iter_inspect] != 1:
            # for ind_op_iter_inspect in range(num_op_job_inspect):
        # for job_inspect in job_inspect_list:
        
        size_set_job_unfinished = len(set_job_unfinished)  
        while size_set_job_unfinished > 0:
            ind_set_op_earliest = np.argmin(job_constraint_set_job_unfinished) 
            op_earliest = idx_op_set_job_unfinished[ind_set_op_earliest] # int(  )
            
            if new_flag_scheduled_ops[op_earliest]  == 1:
                print('unexpected scheduled operation')
            # if new_flag_scheduled_ops[op_earliest]  == 1:
            
            mac_op_earliest = self.mac_assignment_ops[op_earliest]
            ind_job_op_earliest = self.ind_job_ops[op_earliest]
            job_type_op_earliest = self.type_jobs[ind_job_op_earliest]
            ind_op_op_earliest = self.ind_op_ops[op_earliest]
            process_time_op_earliest = self.job_types[job_type_op_earliest][ind_op_op_earliest]['process_time']
            mac_type_op_earliest = self.machine_type_ops[op_earliest]
            if self.flag_mac_available[mac_op_earliest] == 0:
                ind_mac_selected_type_macs = np.argmin(new_ready_time_type_macs[mac_type_op_earliest] + available_mac_offset[mac_type_op_earliest])
                mac_op_earliest = self.machines[mac_type_op_earliest][ind_mac_selected_type_macs]
            # if self.flag_mac_available[mac_op_earliest] == 0:
            
            
            # mac_type_op_earliest = machine_status[mac_op_earliest]['type']
            ind_mac_op_earliest = self.hash_ind_mac_types[mac_op_earliest]
            start_time_candidate = job_constraint_set_job_unfinished[ind_set_op_earliest]
            if start_time_candidate < new_ready_time_type_macs[mac_type_op_earliest][ind_mac_op_earliest]:
                start_time_candidate = new_ready_time_type_macs[mac_type_op_earliest][ind_mac_op_earliest]
            # new_start_time_ops[op_earliest] < new_ready_time_type_macs[mac_type_op_earliest][ind_mac_op_earliest]
            if start_time_candidate < cur_time:
                start_time_candidate = cur_time
            # if new_start_time_ops[op_earliest] < cur_time:
            
            pos_insert_op_schedule = pos_insertion_macs[mac_op_earliest]
            op_priority_ref = op_priority_ref_macs[mac_op_earliest]
            while op_priority_ref != -1:
                max_pend_time_op_priority_ref = self.max_pend_time_ops[op_priority_ref]
                
                if start_time_candidate + process_time_op_earliest <= new_start_time_ops[op_priority_ref]:
                    break
                # if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref]:
                
                ind_job_priority = self.ind_job_ops[op_priority_ref]
                ind_op_op_priority = self.ind_op_ops[op_priority_ref]
                job_constraint_op_priority = self.arrival_time_jobs[ind_job_priority]
                if ind_op_op_priority > 0:
                    job_constraint_op_priority = new_end_time_ops[op_priority_ref - 1]
                # if ind_op_op_priority > 0:    
                
                if start_time_candidate < new_start_time_ops[op_priority_ref] and start_time_candidate + process_time_op_earliest > new_start_time_ops[op_priority_ref]  and start_time_candidate + process_time_op_earliest <= job_constraint_op_priority + max_pend_time_op_priority_ref * self.perc_pend_time:
                    sentinel_feasible, start_time_ops_trial, end_time_ops_trial, start_time_op_macs_trial, end_time_op_macs_trial, ready_time_type_macs_trial = self.postpone_operation(cur_time, machine_status, op_priority_ref, start_time_candidate, process_time_op_earliest,  new_start_time_ops, new_end_time_ops, new_start_time_op_macs, new_end_time_op_macs, new_ready_time_type_macs, new_mac_assignment_ops, new_op_seq_machines, new_op_anchor_type_macs)
                    if sentinel_feasible == True:
                        new_start_time_ops = start_time_ops_trial # copy.deepcopy(start_time_ops)
                        new_end_time_ops = end_time_ops_trial # copy.deepcopy(end_time_ops)
                        new_start_time_op_macs = start_time_op_macs_trial # copy.deepcopy(start_time_op_macs)
                        new_end_time_op_macs = end_time_op_macs_trial # copy.deepcopy(end_time_op_macs)
                        new_ready_time_type_macs = ready_time_type_macs_trial # copy.deepcopy(ready_time_type_macs)
                        break
                    # if sentinel_feasible == True:
                # if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref] + max_pend_time_op_priority_ref:
                
                if new_end_time_ops[op_priority_ref] > start_time_candidate:
                    start_time_candidate = new_end_time_ops[op_priority_ref]
                # if end_time_ops[op_priority_ref] > start_time_candidate:
                
                pos_insert_op_schedule = pos_insert_op_schedule + 1
                while pos_insert_op_schedule < len(new_op_seq_machines[mac_op_earliest]):
                    op_temp = new_op_seq_machines[mac_op_earliest][pos_insert_op_schedule]
                    ind_job_op_temp = int( self.ind_job_ops[op_temp] )
                    job_temp = self.name_jobs[ind_job_op_temp]
                    if job_status[job_temp]['priority'] > 0: 
                        op_priority_ref = op_temp
                        break
                    # if job_status[job_temp]['priority'] > 0: 
                    pos_insert_op_schedule = pos_insert_op_schedule + 1
                # while pos_insert_op_schedule < len(op_seq_machines[mac_op_earliest])
                if pos_insert_op_schedule >= len(new_op_seq_machines[mac_op_earliest]):
                    op_priority_ref = -1
                    break
                # if pos_insert_op_schedule >= len(op_seq_machines[mac_op_earliest]):                  
            # while op_priority_ref != -1:
                                
            pos_insertion_macs[mac_op_earliest] = pos_insert_op_schedule
            op_priority_ref_macs[mac_op_earliest] = op_priority_ref
            new_start_time_ops[op_earliest] = start_time_candidate
            new_end_time_ops[op_earliest] = new_start_time_ops[op_earliest] + process_time_op_earliest # self.job_types[job_type_init][ind_op_job_temp]['process_time']
            new_op_seq_machines[mac_op_earliest].insert(pos_insert_op_schedule, op_earliest)
            new_job_seq_machines[mac_op_earliest].insert(pos_insert_op_schedule, self.name_jobs[ind_job_op_earliest])
            new_start_time_op_macs[mac_op_earliest].insert(pos_insert_op_schedule, new_start_time_ops[op_earliest])
            new_end_time_op_macs[mac_op_earliest].insert(pos_insert_op_schedule, new_end_time_ops[op_earliest])
            new_ready_time_type_macs[mac_type_op_earliest][ind_mac_op_earliest] = new_end_time_ops[op_earliest]
            new_scheduled_length_mac_types[mac_type_op_earliest] = new_scheduled_length_mac_types[mac_type_op_earliest] + process_time_op_earliest
            
            new_op_anchor_type_macs[mac_op_earliest] = op_earliest
            
            new_mac_assignment_ops[op_earliest] = mac_op_earliest
            new_flag_scheduled_ops[op_earliest] = 1
            pos_insertion_macs[mac_op_earliest] = pos_insertion_macs[mac_op_earliest] + 1
            
            
            
            if op_earliest == final_idx_op_set_job_unfinished[ind_set_op_earliest]:
                set_job_unfinished.pop(ind_set_op_earliest)
                idx_op_set_job_unfinished.pop(ind_set_op_earliest)
                final_idx_op_set_job_unfinished.pop(ind_set_op_earliest)
                job_constraint_set_job_unfinished.pop(ind_set_op_earliest)
            else:
                # op_suc_earliest = op_earliest + 1    
                idx_op_set_job_unfinished[ind_set_op_earliest] = op_earliest + 1
                job_constraint_set_job_unfinished[ind_set_op_earliest] = new_end_time_ops[op_earliest]
            # if op_earliest == final_idx_op_set_job_unfinished[ind_set_op_earliest]:
            
            size_set_job_unfinished = len(set_job_unfinished)  
        # while size_set_job_unfinished > 0:
        
            
        #----------------   Division   ----------------#
        new_total_length_machine_type = self.total_length_machine_type.copy()
        average_length_machine_type = {}
        max_average_length = -1
        # mac_type_max_average_length = None
        for machine_type_temp in self.machines:
            new_total_length_machine_type[machine_type_temp] = new_total_length_machine_type[machine_type_temp] + sum( cumul_pend_time_type_macs[machine_type_temp] )
            
            for ind_mac_type_temp in range(self.num_machine_available_types[machine_type_temp]):
                machine_temp = self.machines[machine_type_temp][ind_mac_type_temp]
                if self.flag_mac_available[machine_temp] == 0:
                    new_total_length_machine_type[machine_type_temp] = new_total_length_machine_type[machine_type_temp] - cumul_pend_time_type_macs[machine_type_temp][ind_mac_type_temp]
                # if self.flag_mac_available[machine_temp] == 0:
            # for ind_mac_type_temp in range(self.num_machine_available_types[machine_type_temp]):
            
            coeff_temp = 1.0 # + ind_mac_type_temp / 10.0
            average_length_machine_type[machine_type_temp] = new_total_length_machine_type[machine_type_temp] * coeff_temp / self.num_machine_available_types[machine_type_temp]
            if average_length_machine_type[machine_type_temp]  > max_average_length:
                max_average_length = average_length_machine_type[machine_type_temp]
                # mac_type_max_average_length = machine_type_temp
            # if average_length_machine_type[machine_type_temp]  > max_average_length:
        # for machine_type_temp in self.machines:
        
        
        num_left_job = np.zeros(self.num_job_types)
        for ind_job_type in range(self.num_job_types):
            job_type_temp = self.keys_job_types[ind_job_type]
            num_left_job[ind_job_type] = self.num_jobs_type_idx[job_type_temp] - self.num_type_job_priority[ind_job_type] - num_scheduled_jobs_per_type[job_type_temp]
            if num_left_job[ind_job_type] < 0:
                print('incorrect number of jobs')
            # if num_dispatch_temp < 0:
        # for ind_job_type in range(self.num_job_types):
        
        
        #----------------      Dispatch      ----------------#            
        for machine_temp in machine_status:
            num_op_mac_temp = len(new_op_seq_machines[machine_temp])
            # ind_last_ordinary_op = 0
            for ind_op_mac in range(num_op_mac_temp):
                op_iter = new_op_seq_machines[machine_temp][ind_op_mac]
                ind_job_op_iter = self.ind_job_ops[op_iter]
                priority_op_iter = self.priority_jobs[ind_job_op_iter]
                if priority_op_iter == 0:
                    new_op_anchor_type_macs[machine_temp] = op_iter
                # if priority_op_iter == 0:
            # for ind_op_mac in range(num_op_mac_temp):
        # for machine_temp in machine_status:
        
        
        while np.sum(new_flag_scheduled_jobs) < self.num_job:
            # machine set
            mac_available_set = {}
            ind_mac_available_set = {}
            buffer_macs = {}
            ready_time_comp = -1
            # idx_mac_max_length = -1
            for machine_type_temp in self.machines:
                ind_mac_type_mac = np.argmin( new_ready_time_type_macs[machine_type_temp] + available_mac_offset[machine_type_temp] )
                
                mac_selected_temp = self.machines[machine_type_temp][ind_mac_type_mac]
                mac_available_set[machine_type_temp] = mac_selected_temp
                ind_mac_available_set[machine_type_temp] = ind_mac_type_mac
                if ready_time_comp == -1:
                    buffer_macs[machine_type_temp] = 0
                    ready_time_comp = new_ready_time_type_macs[machine_type_temp][ind_mac_type_mac]
                else:
                    ready_time_cur = new_ready_time_type_macs[machine_type_temp][ind_mac_type_mac]
                    buffer_macs[machine_type_temp] = ready_time_cur - ready_time_comp
                    ready_time_comp = ready_time_cur
                # if ready_time_comp == -1:
            # for machine_temp in self.machines:
            
            
            # grade the type of jobs
            status_job = 3 * np.ones(self.num_job_types)
            score_job = np.zeros((self.num_job_types, 2))
            for ind_job_type in range(self.num_job_types):
                if num_left_job[ind_job_type] <= 0:
                    continue
                # if num_job_dispatch_mac[idx_mac_max_length, ind_job_type] <= 0:
                
                job_type_temp = self.keys_job_types[ind_job_type]                 
                # sentinel_tardiness = False
                score_tardiness = np.zeros(self.num_kind_mac)
                score_comb = np.zeros(self.num_kind_mac)
                job_constraint_score = 0
                for ind_op_temp in range(self.num_kind_mac):
                    mac_type_cur = self.keys_mac_types[ind_op_temp]
                    idx_mac_cur = ind_mac_available_set[mac_type_cur]
                    mac_score = mac_available_set[mac_type_cur]
                    process_time_cur_mac = self.process_time_mac_jobs[mac_type_cur][job_type_temp]
                    if process_time_cur_mac == -1:
                        process_time_cur_mac = 0
                    # if process_time_cur_mac == -1:
                    urgence_coeff_temp = (1.0 + ind_op_temp * 0.2) * (new_total_length_machine_type[mac_type_cur] - new_scheduled_length_mac_types[mac_type_cur]) / self.num_machine_available_types[mac_type_cur]
                                        
                    start_time_score = job_constraint_score
                    if start_time_score < new_ready_time_type_macs[mac_type_cur][idx_mac_cur]:
                        start_time_score = new_ready_time_type_macs[mac_type_cur][idx_mac_cur]
                    # if start_time_score < ready_time_type_macs[mac_type_cur][idx_mac_cur]:
                    tardiness_temp = start_time_score - new_ready_time_type_macs[mac_type_cur][idx_mac_cur]
                        
                    op_priority_score = op_priority_ref_macs[mac_score]
                    if op_priority_score != -1:
                        max_pend_time_op_priority_score = self.max_pend_time_ops[op_priority_score]
                        if start_time_score + process_time_cur_mac > new_start_time_ops[op_priority_score] + 0.5 * self.perc_pend_time * max_pend_time_op_priority_score:
                            start_time_score = new_end_time_ops[op_priority_score]
                            tardiness_temp = new_start_time_ops[op_priority_score] - new_ready_time_type_macs[mac_type_cur][idx_mac_cur]
                        # if start_time_score + process_time_cur_mac < start_time_ops[op_priority_score]:
                    # if op_priority_score != -1
                            
                    if tardiness_temp > 0:
                        # sentinel_tardiness = True
                        score_tardiness[ind_op_temp] = - tardiness_temp * urgence_coeff_temp
                    # else:
                    if op_priority_score != -1:
                        max_pend_time_op_priority_score = self.max_pend_time_ops[op_priority_score]
                        length_left = new_start_time_ops[op_priority_score] - start_time_score - process_time_cur_mac
                        if length_left > 0:
                            if length_left < self.length_comb_macs[mac_type_cur][0]:
                                score_comb[ind_op_temp] = - length_left * urgence_coeff_temp
                            elif length_left < self.max_length_comb:
                                idx_plus = -1
                                for ind_length_comb in range(len(self.length_comb_macs[mac_type_cur])):
                                    if self.length_comb_macs[mac_type_cur][ind_length_comb] > length_left:
                                        idx_plus = ind_length_comb
                                        break
                                    # end if self.length_comb_macs[mac_type_cur][ind_length_comb] > length_left:
                                # end for ind_length_comb in len(self.length_comb_macs[mac_type_cur]):
                                if idx_plus == 0:
                                    print('incorrect index')
                                elif idx_plus != -1:
                                    length_plus = self.length_comb_macs[mac_type_cur][idx_plus]
                                    length_minus = self.length_comb_macs[mac_type_cur][idx_plus-1]
                                    if length_left > length_minus + 0.1 * self.perc_pend_time * max_pend_time_op_priority_score:
                                        score_comb[ind_op_temp] = - (length_plus - length_left) * urgence_coeff_temp
                                    # end if length_left > length_minus + 0.5 * self.perc_pend_time * max_pend_time_op_priority_score:
                                # end if idx_plus == 0 or idx_plus == -1:
                            # end if length_left < self.length_comb_macs[mac_type_cur][0]:
                        # if length_left > 0:
                    # if op_priority_score != -1
                    # if tardiness_temp > 0:
                        
                    job_constraint_score = start_time_score + process_time_cur_mac
                # for ind_op_temp in range(1, num_op_job_temp):
                
                status_job[ind_job_type] = 2
                score_job[ind_job_type, 1] = coeff_tardiness * np.sum(score_tardiness) + np.sum(score_comb)
            # for ind_job_type in range(self.num_job_types):            
                            
            # select the type of job
            # idx_mac_job_group = idx_mac_max_length
            idx_job_type_selected = -1
            ind_job_selected = -1
            # idx_job_type_first_arrive = -1
            # sentinel_job_type = np.zeros(self.num_job_types)
            idx_job_type_selected = -1
            for ind_job_type in range(self.num_job_types):
                if status_job[ind_job_type] >= 3: #  or sentinel_job_type[ind_job_type] == 1
                    continue
                # if status_job[ind_job_type] >= 4:
                if idx_job_type_selected == -1:
                    idx_job_type_selected = ind_job_type
                else: # if idx_job_type_selected != -1:  
                    if status_job[ind_job_type] < status_job[idx_job_type_selected]:
                        idx_job_type_selected = ind_job_type
                    else:
                        if status_job[ind_job_type] == status_job[idx_job_type_selected]:
                            if status_job[ind_job_type] == 2 and score_job[ind_job_type,1] > score_job[idx_job_type_selected,1]:
                                idx_job_type_selected = ind_job_type
                            # if status_job[ind_job_type] == 2 and score_job[ind_job_type,1] > score_job[idx_job_type_selected,1]:
                            if status_job[ind_job_type] == 1 and score_job[ind_job_type,0] > score_job[idx_job_type_selected,0]:
                                idx_job_type_selected = ind_job_type
                            # if status_job[ind_job_type] == 1 and score_job[ind_job_type,0] > score_job[idx_job_type_selected,0]:
                        # if status_job[ind_job_type] == status_job[idx_job_type_selected]:
                    # if status_job[ind_job_type] < status_job[idx_job_type_selected]:
                # if idx_job_type_selected == -1:
            # for ind_job_type in range(self.num_job_types):    
            
            
            if idx_job_type_selected == -1:
                print('No proper job type')
            # if idx_job_type_selected == -1:
            
            # determine the exact job to be arranged
            job_type_selected = self.keys_job_types[idx_job_type_selected] 
            idx_job_base = self.idx_first_job_types[job_type_selected]
            job_name_selected = None
            for ind_job_selected_type in range(self.num_jobs_type_idx[job_type_selected]):
                if new_flag_scheduled_jobs[idx_job_base + ind_job_selected_type] == 1:
                    continue    
                # if flag_scheduled_jobs[idx_job_base + ind_job_selected_type] == 1 or self.arrival_time_jobs[idx_job_base + ind_job_selected_type] > current_time:
                if self.arrival_time_jobs[idx_job_base + ind_job_selected_type] > 0:
                    continue
                # if self.arrival_time_jobs[idx_job_base + ind_job_selected_type] > current_time:
                if ind_job_selected == -1:
                    ind_job_selected = ind_job_selected_type + idx_job_base
                    job_name_selected = self.name_jobs[ind_job_selected]
                    break
                # if ind_job_selected == -1:
            # for ind_job_selected_type in range(self.num_jobs_type_idx[job_type_selected]):    
            
            if job_type_selected != self.type_jobs[ind_job_selected]:
                print('check job type')
            # if job_type_selected != self.type_jobs[ind_job_selected]:
            
            if ind_job_selected == -1:
                print('No proper job')
            # if ind_job_selected == -1:
                
            # dispatch
            job_constraint_temp = self.arrival_time_jobs[ind_job_selected]
            ind_first_op_temp = self.idx_first_op_jobs[ind_job_selected]
            job_name_selected = self.name_jobs[ind_job_selected]
            num_op_temp = int( self.num_op_jobs[ind_job_selected] )
            for ind_op_job_temp in range(num_op_temp):
                ind_op_schedule = int( ind_first_op_temp + ind_op_job_temp )
                mac_type_temp = self.machine_type_ops[ind_op_schedule]
                process_time_temp = self.job_types[job_type_selected][ind_op_job_temp]['process_time']
                ind_mac_type_mac_temp = ind_mac_available_set[mac_type_temp]
                mac_name_temp = mac_available_set[mac_type_temp]
                
                # determine the start time
                start_time_candidate = job_constraint_temp
                if job_constraint_temp < new_ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp]:
                    start_time_candidate = new_ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp]
                # if job_constraint_temp < ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp]: 
                if start_time_candidate < cur_time:
                    start_time_candidate = cur_time
                # if start_time_candidate < cur_time:
                
                
                pos_insert_op_schedule = pos_insertion_macs[mac_name_temp]
                op_priority_ref = op_priority_ref_macs[mac_name_temp]
                while op_priority_ref != -1:
                    max_pend_time_op_priority_ref = self.max_pend_time_ops[op_priority_ref]
                    
                    if start_time_candidate + process_time_temp <= new_start_time_ops[op_priority_ref]:
                        break
                    # if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref]:
                    
                    ind_job_priority = self.ind_job_ops[op_priority_ref]
                    ind_op_op_priority = self.ind_op_ops[op_priority_ref]
                    job_constraint_op_priority = self.arrival_time_jobs[ind_job_priority]
                    if ind_op_op_priority > 0:
                        job_constraint_op_priority = new_end_time_ops[op_priority_ref - 1]
                    # if ind_op_op_priority > 0:    
                    
                    if start_time_candidate < new_start_time_ops[op_priority_ref] and start_time_candidate + process_time_temp > new_start_time_ops[op_priority_ref]  and start_time_candidate + process_time_temp <= job_constraint_op_priority + max_pend_time_op_priority_ref * self.perc_pend_time:
                        sentinel_feasible, start_time_ops_trial, end_time_ops_trial, start_time_op_macs_trial, end_time_op_macs_trial, ready_time_type_macs_trial = self.postpone_operation(cur_time, machine_status, op_priority_ref, start_time_candidate, process_time_temp,  new_start_time_ops, new_end_time_ops, new_start_time_op_macs, new_end_time_op_macs, new_ready_time_type_macs, new_mac_assignment_ops, new_op_seq_machines, new_op_anchor_type_macs)
                        if sentinel_feasible == True:
                            new_start_time_ops = start_time_ops_trial # copy.deepcopy(start_time_ops)
                            new_end_time_ops = end_time_ops_trial # copy.deepcopy(end_time_ops)
                            new_start_time_op_macs = start_time_op_macs_trial # copy.deepcopy(start_time_op_macs)
                            new_end_time_op_macs = end_time_op_macs_trial # copy.deepcopy(end_time_op_macs)
                            new_ready_time_type_macs = ready_time_type_macs_trial # copy.deepcopy(ready_time_type_macs)
                            break
                        # if sentinel_feasible == True:
                    # if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref] + max_pend_time_op_priority_ref:
                    
                    if new_end_time_ops[op_priority_ref] > start_time_candidate:
                        start_time_candidate = new_end_time_ops[op_priority_ref]
                    # if end_time_ops[op_priority_ref] > start_time_candidate:
                    
                    pos_insert_op_schedule = pos_insert_op_schedule + 1
                    while pos_insert_op_schedule < len(new_op_seq_machines[mac_name_temp]):
                        op_temp = new_op_seq_machines[mac_name_temp][pos_insert_op_schedule]
                        ind_job_op_temp = int( self.ind_job_ops[op_temp] )
                        job_temp = self.name_jobs[ind_job_op_temp]
                        if job_status[job_temp]['priority'] > 0: 
                            op_priority_ref = op_temp
                            break
                        # if job_status[job_temp]['priority'] > 0: 
                        pos_insert_op_schedule = pos_insert_op_schedule + 1
                    # while pos_insert_op_schedule < len(op_seq_machines[mac_name_temp])
                    if pos_insert_op_schedule >= len(new_op_seq_machines[mac_name_temp]):
                        op_priority_ref = -1
                        break
                    # if pos_insert_op_schedule >= len(op_seq_machines[mac_name_temp]):                  
                # while op_priority_ref != -1:
                
                
                
                pos_insertion_macs[mac_name_temp] = pos_insert_op_schedule
                op_priority_ref_macs[mac_name_temp] = op_priority_ref
                new_start_time_ops[ind_op_schedule] = start_time_candidate
                new_end_time_ops[ind_op_schedule] = new_start_time_ops[ind_op_schedule] + process_time_temp # self.job_types[job_type_init][ind_op_job_temp]['process_time']
                new_op_seq_machines[mac_name_temp].insert(pos_insert_op_schedule, ind_op_schedule)
                new_job_seq_machines[mac_name_temp].insert(pos_insert_op_schedule, job_name_selected)
                new_start_time_op_macs[mac_name_temp].insert(pos_insert_op_schedule, new_start_time_ops[ind_op_schedule])
                new_end_time_op_macs[mac_name_temp].insert(pos_insert_op_schedule, new_end_time_ops[ind_op_schedule])
                new_ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp] = new_end_time_ops[ind_op_schedule]
                new_op_anchor_type_macs[mac_name_temp] = ind_op_schedule
                new_scheduled_length_mac_types[mac_type_temp] = new_scheduled_length_mac_types[mac_type_temp] + process_time_temp
                
                new_mac_assignment_ops[ind_op_schedule] = mac_name_temp
                new_flag_scheduled_ops[ind_op_schedule] = 1
                pos_insertion_macs[mac_name_temp] = pos_insertion_macs[mac_name_temp] + 1
                
                job_constraint_temp = new_end_time_ops[ind_op_schedule]
            # for ind_op_job_temp in range(num_op_temp):
            
            new_flag_scheduled_jobs[ind_job_selected] = 1
            num_left_job[idx_job_type_selected] = num_left_job[idx_job_type_selected] - 1
            if num_left_job[idx_job_type_selected] < 0: #  group_job_mac[idx_mac_job_group, idx_job_type_selected] > 0:
               print('incorrect number of job')
            # if num_left_job[idx_job_type_selected] < 0:
        # while np.sum(flag_scheduled_jobs) < self.num_job:
        
        
        #----------------   Recording   ----------------#
        op_max_end_time = np.argmax(new_end_time_ops)
        makespan = new_end_time_ops[op_max_end_time] # np.max(end_time_ops)    
        
        return makespan, new_op_seq_machines, new_job_seq_machines, new_start_time_op_macs, new_end_time_op_macs, new_start_time_ops, new_end_time_ops, new_mac_assignment_ops, new_flag_scheduled_ops, count_scheduled_op_macs, new_flag_scheduled_jobs
    # def generation_resume():
    
    
    
    def init_construction(self, job_status, job_list, machine_status, cur_time):
        #----------------   Preparation   ----------------#
        num_job = len(job_status)
        self.flag_mac_available = {}
        for mac_name_temp in machine_status:
            self.flag_mac_available[mac_name_temp] = 1
        # for mac_name_temp in machine_status:
        
        name_jobs = []
        idx_first_job_types = {}
        type_jobs = []
        num_op_jobs = np.zeros(num_job)
        arrival_time_jobs = []
        priority_jobs = []
        idx_first_op_jobs = -1 * np.ones(num_job) 
        ind_job_ops = []
        ind_op_ops = []
        machine_type_ops = []
        max_pend_time_ops = []
        process_time_ops = []
        
        arrival_jobs_priority = {}
        priority_jobs_priority = {}
        idx_set_job_priority = {}
        num_type_job_priority = np.zeros(self.num_job_types)
        set_job_priority = []
        size_set_job_priority = 0
        
        total_num_ops = 0
        type_record = None
        ind_job = 0
        for job in job_status:
            name_jobs.append(job)
            type_temp = job_status[job]['type']
            if type_record == None or type_temp != type_record:
                type_record = type_temp
                idx_first_job_types[type_record] = ind_job
            # if type_record == None or type_temp != type_record:                
            type_jobs.append(type_temp)
            num_op_temp = self.num_op_job_types[type_temp]
            num_op_jobs[ind_job] = int( num_op_temp )
            arrival_time_jobs.append(job_status[job]['arrival'])
            priority_jobs.append(job_status[job]['priority'])
            idx_first_op_jobs[ind_job] = total_num_ops
            for ind_op_temp in range(num_op_temp):
                ind_job_ops.append(ind_job)
                ind_op_ops.append(ind_op_temp)
                machine_type_ops.append(self.job_types[type_temp][ind_op_temp]['machine_type'])
                max_pend_time_ops.append(self.job_types[type_temp][ind_op_temp]['max_pend_time'])
                process_time_ops.append(self.job_types[type_temp][ind_op_temp]['process_time'])
            # for ind_op_temp in range(num_op_temp):
            
            if job_status[job]['priority'] > 0:
                arrival_jobs_priority[job] = job_status[job]['arrival']
                priority_jobs_priority[job] = job_status[job]['priority']   
                idx_set_job_priority[job] = ind_job
                idx_type_temp = self.hash_ind_job_types[type_temp]
                num_type_job_priority[idx_type_temp] = num_type_job_priority[idx_type_temp] + 1
                
                idx_pos_job_priority = 0
                for ind_job_priority in range(size_set_job_priority):
                    job_comp = set_job_priority[ind_job_priority]
                    if arrival_jobs_priority[job_comp] >= arrival_jobs_priority[job]:
                        break
                    # if arrival_jobs_priority[job_comp] >= arrival_jobs_priority[job]:
                    idx_pos_job_priority = idx_pos_job_priority + 1
                # for ind_job_priority in range(size_set_job_priority):
                set_job_priority.insert(idx_pos_job_priority, job)
                size_set_job_priority = size_set_job_priority + 1
            # if job_status[job]['priority'] > 0:
            total_num_ops = total_num_ops + num_op_temp
            ind_job = ind_job + 1
        # for job in job_status:
            
        num_jobs_type_idx = {}
        for ind_job in range(num_job):
            if type_jobs[ind_job] in num_jobs_type_idx:
                num_jobs_type_idx[ type_jobs[ind_job] ] = num_jobs_type_idx[ type_jobs[ind_job] ] + 1
            else:
                num_jobs_type_idx[ type_jobs[ind_job] ] = 1
            # if type_jobs[ind_job] in num_jobs_type_idx:
        # for ind_job in range(num_job):
            
        num_machine_available_types = {}
        num_op_mac_jobs = {}
        total_length_machine_type = {}
        # average_length_machine_type = {}
        # max_average_length = -1
        # mac_type_max_average_length = None
        for machine_temp in self.machines:
            num_machine_available_types[machine_temp] = len(self.machines[machine_temp])
            num_op_mac_jobs[machine_temp] = {}
            total_length_machine_type[machine_temp] = 0
            for key_job_type in self.key_dict_job_types:                
                if self.process_time_mac_jobs[machine_temp][key_job_type] != -1:
                    total_length_machine_type[machine_temp] = total_length_machine_type[machine_temp] + num_jobs_type_idx[key_job_type] * self.process_time_mac_jobs[machine_temp][key_job_type]
                    num_op_mac_jobs[machine_temp][key_job_type] = num_jobs_type_idx[key_job_type]
                else:
                    num_op_mac_jobs[machine_temp][key_job_type] = 0
                # if processing_time_temp != -1:
            # for key_job_type in key_dict_job_types:
            # coeff_temp = 1.0 # + ind_mac_type_temp / 10.0
            # average_length_machine_type[machine_temp] = total_length_machine_type[machine_temp] * coeff_temp / num_machine_available_types[machine_temp]
            # if average_length_machine_type[machine_temp] > max_average_length:
            #     max_average_length = average_length_machine_type[machine_temp]
            #     mac_type_max_average_length = machine_temp
            # # if average_length_machine_type[machine_temp]  > max_average_length:
        # for machine_temp in self.machines:
        
        self.mac_set_breakdown = []
        self.total_num_ops = total_num_ops
        self.num_job = num_job
        self.num_op_jobs = num_op_jobs
        self.idx_first_job_types = idx_first_job_types
        self.name_jobs = name_jobs
        self.arrival_time_jobs = arrival_time_jobs
        self.priority_jobs = priority_jobs
        self.ind_job_ops = ind_job_ops
        self.ind_op_ops = ind_op_ops
        self.type_jobs = type_jobs
        self.machine_type_ops = machine_type_ops
        self.idx_first_op_jobs = idx_first_op_jobs
        self.num_jobs_type_idx = num_jobs_type_idx    
        self.num_machine_available_types = num_machine_available_types
        self.num_op_mac_jobs = num_op_mac_jobs
        self.total_length_machine_type = total_length_machine_type
        self.max_pend_time_ops = max_pend_time_ops
        self.process_time_ops = process_time_ops
        
        self.set_job_priority = set_job_priority
        self.idx_set_job_priority = idx_set_job_priority
        self.arrival_jobs_priority = arrival_jobs_priority
        self.priority_jobs_priority = priority_jobs_priority
        self.size_set_job_priority = size_set_job_priority
        self.num_type_job_priority = num_type_job_priority  
        
        # coeff_tardiness = 0.5
        
        # start_time = time.time()
        
        manager = multiprocessing.Manager()
        makespan_ct_dict = manager.dict()
        data_ct_dict = manager.dict()
        
        jobs_ct = []
        # set_coeff_tardiness = [1.0, 0.5, 0.2, 0.1, 0.05, 0.01]
        for ind_process in range(6):
            proc = multiprocessing.Process(target=process_generate_scratch, args=(self, cur_time, job_status, machine_status, self.set_coeff_tardiness[ind_process], makespan_ct_dict, data_ct_dict))
            jobs_ct.append(proc)
            proc.start()
        # for ind_process in range(6):
        for proc in jobs_ct:
            proc.join()
        # for proc in jobs:
        ct_min_makespan = min(makespan_ct_dict ,key = makespan_ct_dict.get)
        
        makespan_best = makespan_ct_dict[ct_min_makespan]
        op_seq_machines_best, job_seq_machines_best, start_time_op_macs_best, end_time_op_macs_best, start_time_ops_best, end_time_ops_best, mac_assignment_ops_best, flag_scheduled_ops_best, flag_scheduled_jobs_best = data_ct_dict[ct_min_makespan]
        coeff_tardiness_best = ct_min_makespan
        
        #print(makespan_ct_dict.values())
        #print(ct_min_makespan)
        #print(makespan_ct_dict[ct_min_makespan])
        
        if min(self.num_machine_types.values()) > 2:
            makespan_rnd_dict = manager.dict()
            data_rnd_dict = manager.dict() 
            jobs_rnd = []
            for ind_process in range(6):
                proc = multiprocessing.Process(target=process_iteration_scratch, args=(self, ind_process, cur_time, job_status, machine_status, coeff_tardiness_best, makespan_best, makespan_rnd_dict, data_rnd_dict))
                jobs_rnd.append(proc)
                proc.start()
            # for ind_process in range(6):
            for proc in jobs_rnd:
                proc.join()
            # for proc in jobs:
            ind_rnd_min_makespan = min(makespan_rnd_dict ,key = makespan_rnd_dict.get)
            if makespan_rnd_dict[ind_rnd_min_makespan] < makespan_best:
                makespan_best = makespan_rnd_dict[ind_rnd_min_makespan]
                op_seq_machines_best, job_seq_machines_best, start_time_op_macs_best, end_time_op_macs_best, start_time_ops_best, end_time_ops_best, mac_assignment_ops_best, flag_scheduled_ops_best, flag_scheduled_jobs_best = data_rnd_dict[ind_rnd_min_makespan]
            # if makespan_rnd_dict[ind_rnd_min_makespan] < makespan_best:
        # if len(machine_status > 12):
        
        # makespan, op_seq_machines, job_seq_machines, start_time_op_macs, end_time_op_macs, start_time_ops, end_time_ops, mac_assignment_ops, flag_scheduled_ops, flag_scheduled_jobs = self.generation_scratch(cur_time, job_status, machine_status, coeff_tardiness)
        
        # elapsed_time = (time.time() - start_time)
        # print(elapsed_time)  
        
        # self.group_job_mac = group_job_mac
        self.op_seq_machines = op_seq_machines_best
        self.job_seq_machines = job_seq_machines_best
        self.start_time_op_macs = start_time_op_macs_best
        self.end_time_op_macs = end_time_op_macs_best
        self.start_time_ops = start_time_ops_best
        self.end_time_ops = end_time_ops_best
        self.mac_assignment_ops = mac_assignment_ops_best
        self.flag_scheduled_ops = flag_scheduled_ops_best
        self.flag_scheduled_jobs = flag_scheduled_jobs_best
        
        self.count_scheduled_op_macs = {}
        for machine_temp in self.name_macs:
            self.count_scheduled_op_macs[machine_temp] = 0
        # for machine_temp in key_job_list:
        
            
        #----------------     Verification       ----------------#
        penalty_pending_constraint = 0
        for ind_job_check in range(self.num_job):
            name_job_check = self.name_jobs[ind_job_check]
            type_job_check = self.type_jobs[ind_job_check]
            priority_job_check = job_status[name_job_check]['priority']
            if self.flag_scheduled_jobs[ind_job_check] != 1:
                print('unscheduled job')
            # if flag_scheduled_jobs[flag_scheduled_jobs] != 0:
                
            num_op_job_check = int( self.num_op_jobs[ind_job_check] )
            idx_first_op_job_check = self.idx_first_op_jobs[ind_job_check]
            for ind_op_job_check in range(num_op_job_check):
                op_check = int( idx_first_op_job_check + ind_op_job_check )
                if self.flag_scheduled_ops[op_check] != 1:
                    print('unscheduled_ operation')
                # if flag_scheduled_ops[idx_first_op_job_check + ind_op_job_check] != 1:
                
                if ind_op_job_check > 0:
                    if self.end_time_ops[op_check - 1] > self.start_time_ops[op_check]:
                        print('incorrect start time')
                    #  if end_time_ops[op_check - 1] > start_time_ops[op_check]:
                # if ind_op_job_check > 0:
                
                if priority_job_check > 0:
                    pending_constraint_op = self.job_types[type_job_check][ind_op_job_check]['max_pend_time']
                    
                    time_comp = -1
                    if ind_op_job_check == 0:
                        time_comp = self.arrival_time_jobs[ind_job_check]
                        if time_comp < 0:
                            print('wrong arrival time')
                        # if time_comp <= 0:
                    else:
                        time_comp = self.end_time_ops[op_check - 1]
                    #  if ind_op_job_check == 0:
                        
                    if self.start_time_ops[op_check] - time_comp > pending_constraint_op:
                        print('violate the pending contraint')
                        penalty_pending_constraint = penalty_pending_constraint + priority_job_check * 10 * (self.start_time_ops[op_check] - time_comp - pending_constraint_op)
                    # if end_time_ops[op_check] - time_comp >= pending_constraint_op:
                        
                # if job_status[name_job_check]['priority'] > 0:
                
            # for ind_op_job_check in range(num_op_job_check):
        # for ind_job_check in range(self.num_job):
        for machine_temp in machine_status:
            len_op_seq = len(self.op_seq_machines[machine_temp])
            for ind_op_seq in range(len_op_seq-1):
                if self.end_time_op_macs[machine_temp][ind_op_seq] > self.start_time_op_macs[machine_temp][ind_op_seq+1]:
                    print('Incorrect start time')
                # if new_end_time_op_macs[machine_temp][ind_op_seq] > new_start_time_op_macs[machine_temp][ind_op_seq+1]:
            # for ind_op_seq in range(len_op_seq-1):
        # for machine_temp in machine_status:
            
        print('checkpoint')
    # def init_construction(self, job_status, job_list, machine_status):
    
        
    def generation_scratch(self, cur_time, job_status, machine_status, coeff_tardiness, rnd_mode):
        #----------------     Priority     ----------------#   
        op_seq_machines = {}
        job_seq_machines = {}
        start_time_op_macs = {}
        end_time_op_macs = {}
        mac_assignment_ops = {}
        flag_scheduled_ops = np.zeros(self.total_num_ops)
        # key_job_list = job_list.keys()
        # ready_time_macs = {} # np.zeros(self.total_num_machines)
        op_anchor_type_macs = {}
        for machine_temp in self.name_macs:
            op_seq_machines[machine_temp] = []
            job_seq_machines[machine_temp] = []
            start_time_op_macs[machine_temp] = []
            end_time_op_macs[machine_temp] = []
            op_anchor_type_macs[machine_temp] = -1
            # ready_time_macs[machine_temp] = 0
        # for machine_temp in self.name_macs:
            
        flag_scheduled_jobs = np.zeros(self.num_job)
        start_time_ops = -1 * np.ones(self.total_num_ops)
        end_time_ops = -1 * np.ones(self.total_num_ops)
        ready_time_type_macs = {}
        scheduled_length_mac_types = {}
        for machine_type_temp in self.machines:
            ready_time_type_macs[machine_type_temp] = np.zeros(self.num_machine_types[machine_type_temp]) # [0 for _ in range(self.num_machine_types[machine_type_temp])]
            scheduled_length_mac_types[machine_type_temp] = 0
        # for machine_type_temp in self.machines:
        
        occupy_time_type_macs = {}
        for mac_type_temp in self.machines:
            occupy_time_type_macs[mac_type_temp] = np.zeros(self.num_machine_types[mac_type_temp])
        # for mac_type_temp in self.machines:
        
        for ind_set_job_priority in range(self.size_set_job_priority):
            name_job_priority = self.set_job_priority[ind_set_job_priority]
            idx_job_priority = int( self.idx_set_job_priority[name_job_priority] )
            type_job_priority = self.type_jobs[idx_job_priority]
            num_op_job_priority = int( self.num_op_jobs[idx_job_priority] )
            idx_first_op_job_priority = self.idx_first_op_jobs[idx_job_priority]
            
            job_constraint_temp = self.arrival_jobs_priority[name_job_priority]
            for ind_op_job_priority in range(num_op_job_priority):
                idx_op_schedule = int( idx_first_op_job_priority + ind_op_job_priority )
                mac_type_op_schedule = self.machine_type_ops[idx_op_schedule]
                process_time_op_schedule = self.process_time_mac_jobs[mac_type_op_schedule][type_job_priority]
                pend_time_op_schedule = self.job_types[type_job_priority][ind_op_job_priority]['max_pend_time']
                
                # start_time_final = -1
                # ind_position_final = -1
                count_attempt = 0
                num_mac_same_type = self.num_machine_types[mac_type_op_schedule]
                idx_mac_op_schedule = np.argmin(occupy_time_type_macs[mac_type_op_schedule])
                if rnd_mode == 1:
                    idx_mac_op_schedule = random.randint(0, num_mac_same_type-1)
                # if rnd_mode == 1:
                
                while count_attempt < num_mac_same_type:
                    mac_op_schedule = self.machines[mac_type_op_schedule][idx_mac_op_schedule]
                    ind_position_op_schedule = 0
                    start_time_candidate = -1
                    while ind_position_op_schedule < len(start_time_op_macs[mac_op_schedule]):
                        start_time_candidate = job_constraint_temp
                        if ind_position_op_schedule > 0:
                            if end_time_op_macs[mac_op_schedule][ind_position_op_schedule - 1] > start_time_candidate:
                                start_time_candidate = end_time_op_macs[mac_op_schedule][ind_position_op_schedule - 1]
                            # if start_time_op_macs[mac_op_schedule][ind_position_op_schedule - 1] > start_time_candidate:
                        # if ind_position_op_schedule > 0:
                        if start_time_candidate + process_time_op_schedule <= start_time_op_macs[mac_op_schedule][ind_position_op_schedule]:
                            break
                        # if start_time_candidate + pend_time_op_schedule <= start_time_op_macs[mac_op_schedule][ind_position_op_schedule]:
                        ind_position_op_schedule = ind_position_op_schedule + 1
                    # while ind_position_op_schedule < len(start_time_op_macs[mac_op_schedule]):
                    
                    if ind_position_op_schedule == len(start_time_op_macs[mac_op_schedule]):
                        start_time_candidate = job_constraint_temp
                        if ind_position_op_schedule > 0:
                            if end_time_op_macs[mac_op_schedule][ind_position_op_schedule - 1] > start_time_candidate:
                                start_time_candidate = end_time_op_macs[mac_op_schedule][ind_position_op_schedule - 1]
                            # if start_time_op_macs[mac_op_schedule][ind_position_op_schedule - 1] > start_time_candidate:
                        # if ind_position_op_schedule > 0:
                    # if ind_position_op_schedule == len(start_time_op_macs[mac_op_schedule]):
                    
                    if start_time_candidate == -1:
                        print('incorrect start time')
                    # if start_time_candidate == -1:
                    
                    if start_time_candidate > job_constraint_temp + pend_time_op_schedule:
                        idx_mac_op_schedule = (idx_mac_op_schedule + 1) % num_mac_same_type
                        count_attempt = count_attempt + 1
                    else:
                        # start_time_final = start_time_candidate
                        # ind_position_final = ind_position_op_schedule
                        break
                    # if start_time_candidate > job_constraint_temp + pend_time_op_schedule:
                # while count_attempt < num_mac_same_type
                
                start_time_ops[idx_op_schedule] = start_time_candidate
                end_time_ops[idx_op_schedule] = start_time_candidate + process_time_op_schedule
                op_seq_machines[mac_op_schedule].insert(ind_position_op_schedule, idx_op_schedule)
                job_seq_machines[mac_op_schedule].insert(ind_position_op_schedule, name_job_priority)
                start_time_op_macs[mac_op_schedule].insert(ind_position_op_schedule, start_time_candidate)
                end_time_op_macs[mac_op_schedule].insert(ind_position_op_schedule, end_time_ops[idx_op_schedule])
                mac_assignment_ops[idx_op_schedule] = mac_op_schedule
                flag_scheduled_ops[idx_op_schedule] = 1
                scheduled_length_mac_types[mac_type_op_schedule] = scheduled_length_mac_types[mac_type_op_schedule] + process_time_op_schedule
                occupy_time_type_macs[mac_type_op_schedule][idx_mac_op_schedule] = occupy_time_type_macs[mac_type_op_schedule][idx_mac_op_schedule] + process_time_op_schedule
                
                job_constraint_temp = end_time_ops[idx_op_schedule] 
            # for ind_op_job_priority in range(num_op_job_priority):
            flag_scheduled_jobs[idx_job_priority] = 1
        # for ind_job_priority in range(size_set_job_priority):
            
        #----------------     Division     ----------------#
        average_length_machine_type = {}
        max_average_length = -1
        # mac_type_max_average_length = None
        for machine_temp in self.machines:
            coeff_temp = 1.0 # + ind_mac_type_temp / 10.0
            average_length_machine_type[machine_temp] = self.total_length_machine_type[machine_temp] * coeff_temp / self.num_machine_available_types[machine_temp]
            if average_length_machine_type[machine_temp]  > max_average_length:
                max_average_length = average_length_machine_type[machine_temp]
                # mac_type_max_average_length = machine_temp
            # if average_length_machine_type[machine_temp]  > max_average_length:
        # for machine_temp in self.machines:
        
        
        # num_mac_max_average_length = self.num_machine_available_types[mac_type_max_average_length]
        num_left_job = np.zeros(self.num_job_types)
        for ind_job_type in range(self.num_job_types):
            job_type_temp = self.keys_job_types[ind_job_type]            
            num_left_job[ind_job_type] = self.num_jobs_type_idx[job_type_temp] - self.num_type_job_priority[ind_job_type]
            if num_left_job[ind_job_type] < 0:
                print('incorrect number of jobs')
            # if num_dispatch_temp < 0:
        # for ind_job_type in range(self.num_job_types):
        
        
        
        #----------------      Dispatch      ----------------#
        # num_job_dispatch_mac = group_job_mac.copy()
        
        pos_insertion_macs = {}
        op_priority_ref_macs = {}
        for mac_type_temp in self.machines:
            num_mac_type_temp = self.num_machine_types[mac_type_temp]
            # pos_insertion_type_mac[mac_type_temp] = np.zeros(num_mac_type_temp)
            for ind_mac_type in range(num_mac_type_temp):
                mac_name_temp = self.machines[mac_type_temp][ind_mac_type]
                pos_insertion_macs[mac_name_temp] = 0
                if len(op_seq_machines[mac_name_temp]) > 0:
                    op_priority_ref_macs[mac_name_temp] = int( op_seq_machines[mac_name_temp][0] )
                else: # len(op_seq_machines[mac_name_temp]) == 0:
                    op_priority_ref_macs[mac_name_temp] = -1
                # if len(op_seq_machines[mac_name_temp]) > 0:
            # for ind_mac_type in range(num_mac_type_temp):
        # for mac_type_temp in self.machines:
        
        while np.sum(flag_scheduled_jobs) < self.num_job:
            # machine set
            mac_available_set = {}
            ind_mac_available_set = {}
            buffer_macs = {}
            ready_time_comp = -1
            # idx_mac_max_length = -1
            for machine_type_temp in self.machines:
                ind_mac_type_mac = np.argmin( ready_time_type_macs[machine_type_temp] )
                mac_selected_temp = self.machines[machine_type_temp][ind_mac_type_mac]
                mac_available_set[machine_type_temp] = mac_selected_temp
                ind_mac_available_set[machine_type_temp] = ind_mac_type_mac
                if ready_time_comp == -1:
                    buffer_macs[machine_type_temp] = 0
                    ready_time_comp = ready_time_type_macs[machine_type_temp][ind_mac_type_mac]
                else:
                    ready_time_cur = ready_time_type_macs[machine_type_temp][ind_mac_type_mac]
                    buffer_macs[machine_type_temp] = ready_time_cur - ready_time_comp
                    ready_time_comp = ready_time_cur
                # if ready_time_comp == -1:
            # for machine_temp in self.machines:
            
            
            # grade the type of jobs
            status_job = 3 * np.ones(self.num_job_types)
            score_job = np.zeros((self.num_job_types, 2))
            for ind_job_type in range(self.num_job_types):
                if num_left_job[ind_job_type] <= 0:
                    continue
                # if num_job_dispatch_mac[idx_mac_max_length, ind_job_type] <= 0:
                job_type_temp = self.keys_job_types[ind_job_type]                 
                # sentinel_tardiness = False
                # score_consume = np.zeros(self.num_kind_mac-1)
                score_comb = np.zeros(self.num_kind_mac)
                score_tardiness = np.zeros(self.num_kind_mac)
                job_constraint_score = 0
                for ind_op_temp in range(self.num_kind_mac):
                    mac_type_cur = self.keys_mac_types[ind_op_temp]
                    idx_mac_cur = ind_mac_available_set[mac_type_cur]
                    mac_score = mac_available_set[mac_type_cur]
                    process_time_cur_mac = self.process_time_mac_jobs[mac_type_cur][job_type_temp]
                    if process_time_cur_mac == -1:
                        process_time_cur_mac = 0
                    # if process_time_cur_mac == -1:
                    urgence_coeff_temp = (1.0 + ind_op_temp * 0.2) * (self.total_length_machine_type[mac_type_cur] - scheduled_length_mac_types[mac_type_cur]) / self.num_machine_available_types[mac_type_cur]
                                        
                    start_time_score = job_constraint_score
                    if start_time_score < ready_time_type_macs[mac_type_cur][idx_mac_cur]:
                        start_time_score = ready_time_type_macs[mac_type_cur][idx_mac_cur]
                    # if start_time_score < ready_time_type_macs[mac_type_cur][idx_mac_cur]:
                    tardiness_temp = start_time_score - ready_time_type_macs[mac_type_cur][idx_mac_cur]
                        
                    op_priority_score = op_priority_ref_macs[mac_score]
                    if op_priority_score != -1:
                        max_pend_time_op_priority_score = self.max_pend_time_ops[op_priority_score]
                        if start_time_score + process_time_cur_mac > start_time_ops[op_priority_score] + 0.5 * self.perc_pend_time * max_pend_time_op_priority_score:
                            start_time_score = end_time_ops[op_priority_score]
                            tardiness_temp = start_time_ops[op_priority_score] - ready_time_type_macs[mac_type_cur][idx_mac_cur]
                        # if start_time_score + process_time_cur_mac < start_time_ops[op_priority_score]:
                    # if op_priority_score != -1
                            
                    if tardiness_temp > 0:
                        # sentinel_tardiness = True
                        score_tardiness[ind_op_temp] = - tardiness_temp * urgence_coeff_temp
                    # else:
                    if op_priority_score != -1:
                        max_pend_time_op_priority_score = self.max_pend_time_ops[op_priority_score]
                        length_left = start_time_ops[op_priority_score] - start_time_score - process_time_cur_mac
                        if length_left > 0:
                            if length_left < self.length_comb_macs[mac_type_cur][0]:
                                score_comb[ind_op_temp] = - length_left * urgence_coeff_temp
                            elif length_left < self.max_length_comb:
                                idx_plus = -1
                                for ind_length_comb in range(len(self.length_comb_macs[mac_type_cur])):
                                    if self.length_comb_macs[mac_type_cur][ind_length_comb] > length_left:
                                        idx_plus = ind_length_comb
                                        break
                                    # end if self.length_comb_macs[mac_type_cur][ind_length_comb] > length_left:
                                # end for ind_length_comb in len(self.length_comb_macs[mac_type_cur]):
                                if idx_plus == 0:
                                    print('incorrect index')
                                elif idx_plus != -1:
                                    length_plus = self.length_comb_macs[mac_type_cur][idx_plus]
                                    length_minus = self.length_comb_macs[mac_type_cur][idx_plus-1]
                                    if length_left > length_minus + 0.1 * self.perc_pend_time * max_pend_time_op_priority_score:
                                        score_comb[ind_op_temp] = - (length_plus - length_left) * urgence_coeff_temp
                                    # end if length_left > length_minus + 0.5 * self.perc_pend_time * max_pend_time_op_priority_score:
                                # end if idx_plus == 0 or idx_plus == -1:
                            # end if length_left < self.length_comb_macs[mac_type_cur][0]:
                        # if length_left > 0:
                    # if op_priority_score != -1
                    # if tardiness_temp > 0:
                        
                    job_constraint_score = start_time_score + process_time_cur_mac
                # for ind_op_temp in range(1, num_op_job_temp):
                
                status_job[ind_job_type] = 2
                score_job[ind_job_type, 1] = coeff_tardiness * np.sum(score_tardiness) + np.sum(score_comb)
                
                # if sentinel_tardiness == True:
                #     status_job[ind_job_type] = 2
                #     score_job[ind_job_type, 1] = np.sum(score_tardiness)
                # else:
                #     status_job[ind_job_type] = 1
                #     score_job[ind_job_type, 0] = np.sum(score_comb)
                # # if sentinel_tardiness == True:
            # for ind_job_type in range(self.num_job_types):            
                            
            # select the type of job
            # idx_mac_job_group = idx_mac_max_length
            idx_job_type_selected = -1
            ind_job_selected = -1
            # idx_job_type_first_arrive = -1
            # sentinel_job_type = np.zeros(self.num_job_types)
            idx_job_type_selected = -1
            for ind_job_type in range(self.num_job_types):
                if status_job[ind_job_type] >= 3: #  or sentinel_job_type[ind_job_type] == 1
                    continue
                # if status_job[ind_job_type] >= 4:
                if idx_job_type_selected == -1:
                    idx_job_type_selected = ind_job_type
                else: # if idx_job_type_selected != -1:  
                    if status_job[ind_job_type] < status_job[idx_job_type_selected]:
                        idx_job_type_selected = ind_job_type
                    else:
                        if status_job[ind_job_type] == status_job[idx_job_type_selected]:
                            if status_job[ind_job_type] == 2 and score_job[ind_job_type,1] > score_job[idx_job_type_selected,1]:
                                idx_job_type_selected = ind_job_type
                            # if status_job[ind_job_type] == 2 and score_job[ind_job_type,1] > score_job[idx_job_type_selected,1]:
                            if status_job[ind_job_type] == 1 and score_job[ind_job_type,0] > score_job[idx_job_type_selected,0]:
                                idx_job_type_selected = ind_job_type
                            # if status_job[ind_job_type] == 1 and score_job[ind_job_type,0] > score_job[idx_job_type_selected,0]:
                        # if status_job[ind_job_type] == status_job[idx_job_type_selected]:
                    # if status_job[ind_job_type] < status_job[idx_job_type_selected]:
                # if idx_job_type_selected == -1:
            # for ind_job_type in range(self.num_job_types):    
            
            if idx_job_type_selected == -1:
                print('No proper job type')
            # if idx_job_type_selected == -1:
            
            # determine the exact job to be arranged
            job_type_selected = self.keys_job_types[idx_job_type_selected] 
            idx_job_base = self.idx_first_job_types[job_type_selected]
            job_name_selected = None
            for ind_job_selected_type in range(self.num_jobs_type_idx[job_type_selected]):
                if flag_scheduled_jobs[idx_job_base + ind_job_selected_type] == 1:
                    continue    
                # if flag_scheduled_jobs[idx_job_base + ind_job_selected_type] == 1 or self.arrival_time_jobs[idx_job_base + ind_job_selected_type] > current_time:
                if self.arrival_time_jobs[idx_job_base + ind_job_selected_type] > 0:
                    continue
                # if self.arrival_time_jobs[idx_job_base + ind_job_selected_type] > current_time:
                if ind_job_selected == -1:
                    ind_job_selected = ind_job_selected_type + idx_job_base
                    job_name_selected = self.name_jobs[ind_job_selected]
                    break
                # if ind_job_selected == -1:
            # for ind_job_selected_type in range(self.num_jobs_type_idx[job_type_selected]):    
            
            if job_type_selected != self.type_jobs[ind_job_selected]:
                print('check job type')
            # if job_type_selected != self.type_jobs[ind_job_selected]:
            
            if ind_job_selected == -1:
                print('No proper job')
            # if ind_job_selected == -1:
            
            # dispatch
            job_constraint_temp = self.arrival_time_jobs[ind_job_selected]
            ind_first_op_temp = self.idx_first_op_jobs[ind_job_selected]
            job_name_selected = self.name_jobs[ind_job_selected]
            num_op_temp = int( self.num_op_jobs[ind_job_selected] )
            for ind_op_job_temp in range(num_op_temp):
                ind_op_schedule = int( ind_first_op_temp + ind_op_job_temp )
                mac_type_temp = self.machine_type_ops[ind_op_schedule]
                process_time_temp = self.job_types[job_type_selected][ind_op_job_temp]['process_time']
                ind_mac_type_mac_temp = ind_mac_available_set[mac_type_temp]
                mac_name_temp = mac_available_set[mac_type_temp]
                
                # determine the start time
                start_time_candidate = job_constraint_temp
                if job_constraint_temp < ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp]:
                    start_time_candidate = ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp]
                # if job_constraint_temp < ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp]: 
                
                pos_insert_op_schedule = pos_insertion_macs[mac_name_temp]
                op_priority_ref = op_priority_ref_macs[mac_name_temp]
                
                while op_priority_ref != -1:
                    max_pend_time_op_priority_ref = self.max_pend_time_ops[op_priority_ref]
                    
                    if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref]:
                        break
                    # if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref]:
                    
                    ind_job_priority = self.ind_job_ops[op_priority_ref]
                    ind_op_op_priority = self.ind_op_ops[op_priority_ref]
                    job_constraint_op_priority = self.arrival_time_jobs[ind_job_priority]
                    if ind_op_op_priority > 0:
                        job_constraint_op_priority = end_time_ops[op_priority_ref - 1]
                    # if ind_op_op_priority > 0:
                    
                    if start_time_candidate < start_time_ops[op_priority_ref]  and start_time_candidate + process_time_temp > start_time_ops[op_priority_ref]  and start_time_candidate + process_time_temp <= job_constraint_op_priority + max_pend_time_op_priority_ref * self.perc_pend_time:
                        sentinel_feasible, start_time_ops_trial, end_time_ops_trial, start_time_op_macs_trial, end_time_op_macs_trial, ready_time_type_macs_trial = self.postpone_operation(cur_time, machine_status, op_priority_ref, start_time_candidate, process_time_temp,  start_time_ops, end_time_ops, start_time_op_macs, end_time_op_macs, ready_time_type_macs, mac_assignment_ops, op_seq_machines, op_anchor_type_macs)
                        if sentinel_feasible == True:
                            start_time_ops = start_time_ops_trial # copy.deepcopy(start_time_ops)
                            end_time_ops = end_time_ops_trial # copy.deepcopy(end_time_ops)
                            start_time_op_macs = start_time_op_macs_trial # copy.deepcopy(start_time_op_macs)
                            end_time_op_macs = end_time_op_macs_trial # copy.deepcopy(end_time_op_macs)
                            ready_time_type_macs = ready_time_type_macs_trial # copy.deepcopy(ready_time_type_macs)
                            break
                        # if sentinel_feasible == True:
                    # if start_time_candidate + process_time_temp <= start_time_ops[op_priority_ref] + max_pend_time_op_priority_ref:
                    
                    if end_time_ops[op_priority_ref] > start_time_candidate:
                        start_time_candidate = end_time_ops[op_priority_ref]
                    # if end_time_ops[op_priority_ref] > start_time_candidate:
                    
                    pos_insert_op_schedule = pos_insert_op_schedule + 1
                    while pos_insert_op_schedule < len(op_seq_machines[mac_name_temp]):
                        op_temp = op_seq_machines[mac_name_temp][pos_insert_op_schedule]
                        ind_job_op_temp = int( self.ind_job_ops[op_temp] )
                        job_temp = self.name_jobs[ind_job_op_temp]
                        if job_status[job_temp]['priority'] > 0: 
                            op_priority_ref = op_temp
                            break
                        # if job_status[job_temp]['priority'] > 0: 
                        pos_insert_op_schedule = pos_insert_op_schedule + 1
                    # while pos_insert_op_schedule < len(op_seq_machines[mac_name_temp])
                    if pos_insert_op_schedule >= len(op_seq_machines[mac_name_temp]):
                        op_priority_ref = -1
                        break
                    # if pos_insert_op_schedule >= len(op_seq_machines[mac_name_temp]):                  
                # while op_priority_ref != -1:
                
                
                pos_insertion_macs[mac_name_temp] = pos_insert_op_schedule
                op_priority_ref_macs[mac_name_temp] = op_priority_ref
                start_time_ops[ind_op_schedule] = start_time_candidate
                end_time_ops[ind_op_schedule] = start_time_ops[ind_op_schedule] + process_time_temp # self.job_types[job_type_init][ind_op_job_temp]['process_time']
                op_seq_machines[mac_name_temp].insert(pos_insert_op_schedule, ind_op_schedule)
                job_seq_machines[mac_name_temp].insert(pos_insert_op_schedule, job_name_selected)
                start_time_op_macs[mac_name_temp].insert(pos_insert_op_schedule, start_time_ops[ind_op_schedule])
                end_time_op_macs[mac_name_temp].insert(pos_insert_op_schedule, end_time_ops[ind_op_schedule])
                ready_time_type_macs[mac_type_temp][ind_mac_type_mac_temp] = end_time_ops[ind_op_schedule]
                op_anchor_type_macs[mac_name_temp] = ind_op_schedule
                scheduled_length_mac_types[mac_type_temp] = scheduled_length_mac_types[mac_type_temp] + process_time_temp
                
                mac_assignment_ops[ind_op_schedule] = mac_name_temp
                flag_scheduled_ops[ind_op_schedule] = 1
                pos_insertion_macs[mac_name_temp] = pos_insertion_macs[mac_name_temp] + 1
                
                job_constraint_temp = end_time_ops[ind_op_schedule]
            # for ind_op_job_temp in range(num_op_temp):
            
            flag_scheduled_jobs[ind_job_selected] = 1
            num_left_job[idx_job_type_selected] = num_left_job[idx_job_type_selected] - 1
            if num_left_job[idx_job_type_selected] < 0:
                print('the number of jobs is less than zero')
            # if num_job_dispatch_mac[idx_mac_job_group, idx_job_type_selected] < 0:
        # while np.sum(flag_scheduled_jobs) < self.num_job:
        
            
        #----------------     Recording       ----------------#
        op_max_end_time = np.argmax(end_time_ops)
        makespan = end_time_ops[op_max_end_time] # np.max(end_time_ops)  
        
        return makespan, op_seq_machines, job_seq_machines, start_time_op_macs, end_time_op_macs, start_time_ops, end_time_ops, mac_assignment_ops, flag_scheduled_ops, flag_scheduled_jobs
    # def generation_scratch(self, cur_time, job_status, machine_status):
        
    
    
    def postpone_operation(self, cur_time, machine_status, op_priority_ref, start_time_candidate, process_time_temp,  start_time_ops, end_time_ops, start_time_op_macs, end_time_op_macs, ready_time_type_macs, mac_assignment_ops, op_seq_machines, op_anchor_type_macs):
        sentinel_feasible = True
        
        start_time_ops_trial = copy.deepcopy(start_time_ops)
        end_time_ops_trial = copy.deepcopy(end_time_ops)
        start_time_op_macs_trial = copy.deepcopy(start_time_op_macs)
        end_time_op_macs_trial = copy.deepcopy(end_time_op_macs)
        ready_time_type_macs_trial = copy.deepcopy(ready_time_type_macs)
        
        
        # update the start time and the end time of the postponed operation
        ind_job_op_priority_ref = self.ind_job_ops[op_priority_ref]
        ind_op_op_priority_ref = self.ind_op_ops[op_priority_ref]
        mac_op_priority_ref = mac_assignment_ops[op_priority_ref]
        process_time_op_priority_ref = self.process_time_ops[op_priority_ref]
        start_time_ops_trial[op_priority_ref] = start_time_candidate + process_time_temp
        end_time_ops_trial[op_priority_ref] = start_time_ops_trial[op_priority_ref] + process_time_op_priority_ref
        if op_priority_ref not in op_seq_machines[mac_op_priority_ref]:
            print('wrong processing sequence')
        # if op_priority_ref not in op_seq_machines[mac_op_priority_ref]:
        idx_seq_op_priority_ref = op_seq_machines[mac_op_priority_ref].index(op_priority_ref)
        start_time_op_macs_trial[mac_op_priority_ref][idx_seq_op_priority_ref] = start_time_ops_trial[op_priority_ref]
        end_time_op_macs_trial[mac_op_priority_ref][idx_seq_op_priority_ref] = end_time_ops_trial[op_priority_ref]
        
        
        # simulate the influence
        mac_influence_list = []
        ind_influence_list = []
        if idx_seq_op_priority_ref + 1 < len(op_seq_machines[mac_op_priority_ref]):
            if end_time_ops_trial[op_priority_ref] > start_time_op_macs_trial[mac_op_priority_ref][idx_seq_op_priority_ref + 1]:
                mac_influence_list.append(mac_op_priority_ref)
                ind_influence_list.append(idx_seq_op_priority_ref + 1)
            # if end_time_ops_trial[op_priority_ref] > start_time_op_macs_trial[mac_op_priority_ref][idx_seq_op_priority_ref + 1]:
        # if idx_seq_op_priority_ref + 1 < len(op_seq_machines[mac_op_priority_ref]):
        if ind_op_op_priority_ref + 1 < self.num_op_jobs[ind_job_op_priority_ref]:
            op_suc_temp = op_priority_ref + 1
            if start_time_ops_trial[op_suc_temp] != -1:
                if end_time_ops_trial[op_priority_ref] > start_time_ops_trial[op_suc_temp]:
                    mac_op_suc = mac_assignment_ops[op_suc_temp]
                    idx_seq_op_suc = op_seq_machines[mac_op_suc].index(op_suc_temp)
                    mac_influence_list.append(mac_op_suc)
                    ind_influence_list.append(idx_seq_op_suc)
                # if end_time_ops_trial[op_priority_ref] > start_time_ops_trial[op_suc_temp]:
            # if start_time_ops_trial[op_suc_temp] != -1:
        # if ind_op_op_priority_ref + 1 < self.num_op_jobs[ind_job_op_priority_ref]:
        
        
        while len(mac_influence_list) > 0:
            mac_alter_op = mac_influence_list[0]
            idx_alter_op = ind_influence_list[0]
            
            op_alter = op_seq_machines[mac_alter_op][idx_alter_op]
            ind_job_op_alter = self.ind_job_ops[op_alter]
            # name_job_op_alter = self.name_jobs[ind_job_op_alter]
            # job_type_op_alter = self.type_jobs[ind_job_op_alter] # job_status[name_job_op_alter]['type']
            ind_op_op_alter = self.ind_op_ops[op_alter]
            process_time_alter = self.process_time_ops[op_alter]  # self.job_types[job_type_op_alter][ind_op_op_alter]['process_time']
            if idx_alter_op > 0:
                start_time_ops_trial[op_alter] = end_time_op_macs_trial[mac_alter_op][idx_alter_op - 1]
            else:
                start_time_ops_trial[op_alter] = 0
            # if idx_alter_op > 0:       
            
            
            max_pend_time_op_alter = self.max_pend_time_ops[op_alter]
            job_constraint_op_alter = self.arrival_time_jobs[ind_job_op_alter]
            if ind_op_op_alter > 0:
                job_constraint_op_alter = end_time_ops_trial[op_alter - 1]
            # if ind_op_op_alter > 0:
            if job_constraint_op_alter > start_time_ops_trial[op_alter]:
                start_time_ops_trial[op_alter] = job_constraint_op_alter
            # if end_time_ops[op_alter - 1] > 
            if start_time_ops_trial[op_alter] < cur_time:
                start_time_ops_trial[op_alter] = cur_time
            # if start_time_ops_trial[op_alter] < cur_time:
            
                
            if self.priority_jobs[ind_job_op_alter] > 0 and start_time_ops_trial[op_alter] > job_constraint_op_alter + max_pend_time_op_alter:
                sentinel_feasible = False 
                break
            # if start_time_ops_trial[op_alter] > job_constraint_op_alter + max_pend_time_op_alter:
            
            
            end_time_ops_trial[op_alter] = start_time_ops_trial[op_alter] + process_time_alter
            start_time_op_macs_trial[mac_alter_op][idx_alter_op] = start_time_ops_trial[op_alter]
            end_time_op_macs_trial[mac_alter_op][idx_alter_op] = end_time_ops_trial[op_alter] 
            
            mac_type_op_alter = machine_status[mac_alter_op]['type']
            hash_ind_mac_op_alter = self.hash_ind_mac_types[mac_alter_op]
            if op_anchor_type_macs[mac_alter_op] == op_alter:
                ready_time_type_macs_trial[mac_type_op_alter][hash_ind_mac_op_alter] = end_time_ops_trial[op_alter]
            # if op_anchor_type_macs[mac_alter_op] == op_alter:
            
            if idx_alter_op + 1 < len(op_seq_machines[mac_alter_op]):
                if end_time_ops_trial[op_alter] > start_time_op_macs_trial[mac_alter_op][idx_alter_op + 1]:
                    mac_influence_list.append(mac_alter_op)
                    ind_influence_list.append(idx_alter_op+1)
                # if end_time_ops_trial[op_alter] > start_time_op_macs_trial[mac_alter_op][idx_alter_op + 1]:
            # if idx_alter_op + 1 == len(op_seq_machines[mac_alter_op]):
            
            if ind_op_op_alter + 1 < self.num_op_jobs[ind_job_op_alter]:
                op_suc_temp = op_alter + 1
                
                if start_time_ops_trial[op_suc_temp] != -1:
                    if end_time_ops_trial[op_alter] > start_time_ops_trial[op_suc_temp]:
                        mac_op_suc = mac_assignment_ops[op_suc_temp]
                        pos_op_suc = op_seq_machines[mac_op_suc].index(op_suc_temp)
                        mac_influence_list.append(mac_op_suc)
                        ind_influence_list.append(pos_op_suc)
                    # if end_time_ops[op_alter] > 
                # if start_time_ops_trial[op_suc_temp] != -1:
            # if ind_op_op_alter + 1 < self.num_op_jobs[ind_job_op_alter]:
                
            mac_influence_list.pop(0)
            ind_influence_list.pop(0)
        # while len(mac_influence_list) > 0:
            
        return sentinel_feasible, start_time_ops_trial, end_time_ops_trial, start_time_op_macs_trial, end_time_op_macs_trial, ready_time_type_macs_trial 
    # def postpone_operation(self, cur_time, machine_status, op_priority_ref, start_time_candidate, process_time_temp,  start_time_ops, end_time_ops, start_time_op_macs, end_time_op_macs, ready_time_type_macs, mac_assignment_ops, op_seq_machines, op_anchor_type_macs):
    
        
    def priority_backward(self, cur_time, new_start_time_ops, new_end_time_ops, new_start_time_op_macs, new_end_time_op_macs, ind_op_job_priority, start_time_candidate, pend_time_op_schedule, idx_first_op_job_priority, idx_job_priority, new_mac_assignment_ops, new_op_seq_machines):
        sentinel_feasible = False
        
        start_time_ops_trial = copy.deepcopy(new_start_time_ops)
        end_time_ops_trial = copy.deepcopy(new_end_time_ops)
        start_time_op_macs_trial = copy.deepcopy(new_start_time_op_macs)
        end_time_op_macs_trial = copy.deepcopy(new_end_time_op_macs)
        # ready_time_type_macs_trial = copy.deepcopy(ready_time_type_macs)
        
        ind_op_backward = ind_op_job_priority - 1
        start_time_op_cur = start_time_candidate
        pend_time_op_cur = pend_time_op_schedule
        while ind_op_backward >= 0:
            op_pred = int(idx_first_op_job_priority + ind_op_backward)
            earliest_end_time_op_pred = start_time_op_cur - pend_time_op_cur
            earliest_start_time_op_pred = earliest_end_time_op_pred - self.process_time_ops[op_pred]
            mac_op_pred = new_mac_assignment_ops[op_pred]
            pos_mac_op_pred = new_op_seq_machines[mac_op_pred].index(op_pred)
            
            if start_time_ops_trial[op_pred] < cur_time or earliest_start_time_op_pred < cur_time:
                break
            #  if new_start_time_ops[op_pred] < cur_time:
            
            if start_time_ops_trial[op_pred] > earliest_start_time_op_pred:
                print('incorrect backward')
            else:
                start_time_ops_trial[op_pred] = earliest_start_time_op_pred
                end_time_ops_trial[op_pred] = earliest_end_time_op_pred
                start_time_op_macs_trial[mac_op_pred][pos_mac_op_pred] = earliest_start_time_op_pred
                end_time_op_macs_trial[mac_op_pred][pos_mac_op_pred] = earliest_end_time_op_pred
            # if new_start_time_ops[op_pred] > earliest_start_time_op_pred:
            
            job_constraint_op_pred = self.arrival_time_jobs[idx_job_priority]
            if ind_op_backward > 0:
                job_constraint_op_pred = end_time_ops_trial[op_pred-1]
            # if ind_op_backward > 0:
            pend_time_op_pred = self.max_pend_time_ops[op_pred]
            
            if earliest_start_time_op_pred <= job_constraint_op_pred + pend_time_op_pred:
                sentinel_feasible = True
                break
            # if earliest_start_time_op_pred <= job_constraint_op_pred + pend_time_op_pred:
            
            start_time_op_cur = earliest_start_time_op_pred
            pend_time_op_cur = pend_time_op_pred
            ind_op_backward = ind_op_backward - 1
        # while ind_op_backward > 0:
        
        return sentinel_feasible, start_time_ops_trial, end_time_ops_trial, start_time_op_macs_trial, end_time_op_macs_trial
    # def priority_backward
    
    


