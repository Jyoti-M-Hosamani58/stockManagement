import logging
from venv import logger

from django.db import IntegrityError
from django.db.models import Max, F, Sum
from django.http import JsonResponse
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from hp_app.models import Department,Jobrole,Login,Employee,Machine,Spareparts,Vendor,Stock,Item,StocktoDept,DepttoDept, Deptstock
from django.contrib import messages  # Import messages

# Create your views here.

def index(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            udata = Login.objects.get(username=username)
            if password == udata.password:  # Use hashed password checks in production
                request.session['username'] = username
                request.session['utype'] = udata.utype

                if udata.utype == 'user':
                    return redirect('index')  # Redirect to a user-specific page
                if udata.utype == 'admin':
                    return redirect('admin_dashboard')  # Adjust as necessary
                if udata.utype == 'employee':
                    return redirect('emp_dashboard')  # Adjust as necessary
            else:
                messages.error(request, 'Invalid password')
        except Login.DoesNotExist:
            messages.error(request, 'Invalid Username')

    return render(request, 'index.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def emp_dashboard(request):
    return render(request, 'admin_dashboard.html')


def branch(request):
    if request.method == 'POST':
        branchname = request.POST.get('dept')

        Department.objects.create(department=branchname)


        return redirect('branch')  # Adjust this redirect as needed
    branches = Department.objects.all()  # Fetch all branch records from the database

    return render(request, 'branch.html', {'branches': branches})




def edit_branch(request, branch_id):
    # Get the branch object to edit
    branch = get_object_or_404(Department, id=branch_id)

    # Handle form submission
    if request.method == 'POST':
        # Manually retrieve and update the branch fields
        branch.department = request.POST.get('dept')

        branch.save()
        return redirect('branch')  # Redirect to the branch list after saving

    # Prepopulate form fields for the GET request
    return render(request, 'edit_branch.html', {'branch': branch})

def emp_list(request):
    # Fetch all employees
    employees = Employee.objects.all()

    # Pass the employees list to the template
    return render(request, 'emp_list.html', {'employees': employees})


def edit_employee(request, id):
    # Retrieve the employee object based on the provided ID
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        # Update employee fields directly from the POST data
        employee.fullname = request.POST.get('fullname')
        employee.gender = request.POST.get('gender')
        employee.email = request.POST.get('email')
        employee.city = request.POST.get('city')
        employee.state = request.POST.get('state')
        employee.taluk = request.POST.get('taluk')
        employee.district = request.POST.get('district')
        employee.pincode = request.POST.get('pincode')
        employee.contact = request.POST.get('contact')
        employee.role = request.POST.get('role')

        # Save the updated employee object
        employee.save()
        return redirect('employee_list')  # Redirect to the employee list page

    # Render the edit employee form template with the current employee data
    return render(request, 'edit_employee.html', {'employee': employee})


def generate_employee_id():
    # Fetch the last employee_id (max value) from the Employee model
    last_employee = Employee.objects.aggregate(max_id=Max('emp_id'))
    last_id = last_employee['max_id']

    # Check if we have any employees
    if last_id and last_id.startswith('MI'):
        # Extract the numeric part from the last employee ID, e.g., MI01 -> 1
        numeric_part = int(last_id[2:])  # Strip the 'MI' and convert to int
        new_numeric_part = numeric_part + 1
    else:
        new_numeric_part = 1  # Start from MI01 if no employee exists

    # Generate the new employee ID with the 'MI' prefix and leading zero padding
    new_employee_id = f'MI{new_numeric_part:02d}'  # E.g., MI01, MI02, etc.
    return new_employee_id
 # Ensure you have this utility



def employee(request):
    if request.method == 'POST':
        # Get employee details from the form
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        nationality = request.POST.get('nationality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        Taluk = request.POST.get('Taluk')
        email = request.POST.get('email')
        adhar = request.POST.get('adhar')
        pancard = request.POST.get('pancard')
        doj = request.POST.get('doj')
        pf = request.POST.get('pf')
        tenthpass = request.POST.get('tenthpass')
        tenth_percentage = request.POST.get('tenth_percentage')
        twelfth_pass = request.POST.get('twelfth_pass')
        twelfth_percentage = request.POST.get('twelfth_percentage')
        degree = request.POST.get('degree')
        degreepass = request.POST.get('degreepass')
        degree_percentage = request.POST.get('degree_percentage')
        bank_name = request.POST.get('bank_name')
        bank_account_number = request.POST.get('bank_account_number')
        ifsc_code = request.POST.get('ifsc_code')
        account_holder_name = request.POST.get('account_holder_name')
        password = request.POST.get('password')
        jobRole = request.POST.get('jobRole')
        emp_id = generate_employee_id()  # You need to implement this function

        # Get the branch selected by the user
        branch_id = request.POST.get('branchname')

        # File uploads
        adhar_doc = request.FILES.get('adhar_doc')
        pan_doc = request.FILES.get('pan_doc')
        bank_doc = request.FILES.get('bank_doc')
        photo = request.FILES.get('photo')

        # Save Employee object
        employee = Employee.objects.create(
            fullname=fullname,
            gender=gender,
            dob=dob,
            contact=contact,
            nationality=nationality,
            city=city,
            state=state,
            pincode=pincode,
            district=district,
            Taluk=Taluk,
            email=email,
            adhar=adhar,
            pancard=pancard,

            jrole=jobRole,
            doj=doj,
            pf=pf,
            adhar_doc=adhar_doc,
            pan_doc=pan_doc,
            bank_doc=bank_doc,
            tenthpass=tenthpass,
            tenth_percentage=tenth_percentage,
            twelfth_pass=twelfth_pass,
            twelfth_percentage=twelfth_percentage,
            degree=degree,
            degreepass=degreepass,
            degree_percentage=degree_percentage,
            photo=photo,
            bank_name=bank_name,
            bank_account_number=bank_account_number,
            ifsc_code=ifsc_code,
            account_holder_name=account_holder_name,
            password=password,
            emp_id=emp_id,
            branchname=branch_id,
        )

        # Save Login details
        Login.objects.create(
            username=emp_id,
            password=password,
            utype='employee',
            employee_name=fullname
        )

        return redirect('employee')  # Redirect after saving, adjust URL as needed

    # Get all branches from the database to display in the form
    branches = Department.objects.all()
    jobRole = Jobrole.objects.all()

    return render(request, 'employee.html', {'branches': branches,'jobRole':jobRole})



def jobRole(request):
    if request.method == 'POST':

        jobRole = request.POST.get('jobRole')
        branchname = request.POST.get('branchname')

        Jobrole.objects.create(department=branchname,jobRole=jobRole)


        return redirect('jobRole')  # Adjust this redirect as needed
    branches = Jobrole.objects.all()  # Fetch all branch records from the database
    dept = Department.objects.all()  # Fetch all branch records from the database

    return render(request, 'jobRole.html', {'branches': branches,'dept':dept})





def edit_role(request, branch_id):
    # Get the branch object to edit
    branch = get_object_or_404(Jobrole, id=branch_id)

    # Handle form submission
    if request.method == 'POST':
        # Manually retrieve and update the branch fields
        branch.department = request.POST.get('branchname')
        branch.jobRole = request.POST.get('jobRole')

        branch.save()
        return redirect('jobRole')  # Redirect to the branch list after saving

    # Prepopulate form fields for the GET request
    branches = Jobrole.objects.all()  # Fetch all branch records from the database

    return render(request, 'edit_role.html', {'branch': branch,'branches':branches})

def view_certificate(request, id):
    employee = get_object_or_404(Employee, pk=id)
    return render(request, 'view_certificate.html', {'employee': employee})

    # Render the template with the employee data
    return render(request, 'employee_view.html', {'employee': employee})

def machine(request):
    if request.method == 'POST':

        machine = request.POST.get('machine')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')


        Machine.objects.create(machine=machine,description=description,machinephoto=photo)


        return redirect('machine')  # Adjust this redirect as needed
    machine = Machine.objects.all()  # Fetch all branch records from the database
    return render(request, 'machine.html', {'machine': machine})


def edit_machine(request, id):
    # Get the branch object to edit
    machine= get_object_or_404(Machine, id=id)

    # Handle form submission
    if request.method == 'POST':
        # Manually retrieve and update the branch fields
        machine.machine = request.POST.get('machine')
        machine.description = request.POST.get('description')

        machine.save()
        return redirect('machine')  # Redirect to the branch list after saving

    # Prepopulate form fields for the GET request

    return render(request, 'edit_machine.html', {'machine': machine})



from django.core.files.storage import FileSystemStorage


def spareParts(request):
    if request.method == 'POST':
        machine_name = request.POST.get('machine')
        spare_parts_to_create = []

        # Iterate through each row
        for i in range(1, len(request.POST) + 1):
            spare_part_name = request.POST.get(f'sparetpart_{i}')
            spare_part_no = request.POST.get(f'sparetpartNo_{i}')
            description = request.POST.get(f'description_{i}')
            photo = request.FILES.get(f'photo_{i}')  # Get the uploaded photo

            # Ensure that all fields are valid before saving
            if spare_part_name and photo:
                spare_part = Spareparts(
                    machine=machine_name,
                    sparepart=spare_part_name,
                    sparepartNo=spare_part_no,
                    description=description,
                    sparephoto=photo  # Save the uploaded photo
                )
                spare_parts_to_create.append(spare_part)

        # Bulk save all spare parts
        if spare_parts_to_create:
            Spareparts.objects.bulk_create(spare_parts_to_create)

        return redirect('spareParts')  # Redirect to the spare parts list page

    # Get available machines for the select dropdown
    machines = Machine.objects.all()

    # Get all spare parts and items
    spareparts = Spareparts.objects.all()
    item = Item.objects.all()

    # Fetch all spare parts, including those without matching items
    matching_spare_parts = []
    for sparepart in spareparts:
        # Try to find matching items in the Item table
        matching_items = item.filter(sparePart=sparepart.sparepart)

        # If there are matching items, include them, otherwise set issuedqty to None
        if matching_items.exists():
            matching_spare_parts.append({
                'sparepart': sparepart,
                'matching_items': matching_items
            })
        else:
            matching_spare_parts.append({
                'sparepart': sparepart,
                'matching_items': None  # No matching items, so set issuedqty to None
            })

    return render(request, 'spareParts.html', {
        'machines': machines,
        'spareparts': spareparts,
        'matching_spare_parts': matching_spare_parts
    })

def edit_spare(request, id):
    # Get the Spareparts object to edit
    spareParts = get_object_or_404(Spareparts, id=id)

    # Get the corresponding Item object based on sparepartNo and sparetpart
    sparetpart = spareParts.sparepart
    sparepartNo = spareParts.sparepartNo

    try:
        item = Item.objects.get(sparePartNo=sparepartNo, sparePart=sparetpart)
    except Item.DoesNotExist:
        item = None  # Item does not exist; we may create it later

    # Handle form submission
    if request.method == 'POST':
        # Update Spareparts model fields
        spareParts.machine = request.POST.get('machine')
        spareParts.sparetpart = request.POST.get('sparetpart')
        spareParts.sparepartNo = request.POST.get('sparepartNo')
        spareParts.description = request.POST.get('description')
        spareParts.save()

        # Update or create Item model fields
        new_sparepart = request.POST.get('sparetpart')
        new_sparepartNo = request.POST.get('sparepartNo')

        if item:  # Update existing item
            item.sparePart = new_sparepart
            item.sparePartNo = new_sparepartNo
            item.save()
        else:  # Create a new item if it doesn't exist
            try:
                Item.objects.create(
                    sparePart=new_sparepart,
                    sparePartNo=new_sparepartNo,
                    issuedqty=0  # Default or placeholder value, update as needed
                )
            except IntegrityError as e:
                # Handle any unique constraint or database issues here
                print(f"Error creating Item: {e}")

        return redirect('spareParts')  # Redirect to the spare parts list after saving

    # Prepopulate form fields for the GET request
    machine = Machine.objects.all()  # Fetch all machine records from the database

    return render(request, 'edit_spare.html', {'spareParts': spareParts, 'machine': machine})

def vendor(request):
    if request.method == 'POST':
        vendorName = request.POST.get('vendorName')
        companyName = request.POST.get('companyName')
        vendorAddress = request.POST.get('companyAddress')
        vendorPhone = request.POST.get('vendorPhone')
        companyPhone = request.POST.get('companyPhones')

        Vendor.objects.create(vendorName=vendorName,
                                  companyName=companyName,
                                  vendorAddress=vendorAddress,
                                  vendorPhone=vendorPhone,
                                  companyPhone=companyPhone
                                  )


        return redirect('vendor')  # Adjust this redirect as needed
    vendor = Vendor.objects.all()  # Fetch all branch records from the database

    return render(request, 'vendor.html', {'vendor': vendor})

def edit_vendor(request, id):
    # Get the branch object to edit
    branch = get_object_or_404(Vendor, id=id)

    # Handle form submission
    if request.method == 'POST':
        # Manually retrieve and update the branch fields
        branch.vendorName = request.POST.get('vendorName')
        branch.companyName = request.POST.get('companyName')
        branch.vendorAddress = request.POST.get('vendorAddress')
        branch.companyPhone = request.POST.get('companyPhone')
        branch.vendorAddress = request.POST.get('vendorAddress')

        branch.save()
        return redirect('vendor')  # Redirect to the branch list after saving

    # Prepopulate form fields for the GET request
    return render(request, 'edit_vendor.html', {'branch': branch})

def entryHistory(request):
    if request.method == 'POST':
        print("POST Data:", request.POST)

        last_entryId = Stock.objects.aggregate(Max('entryId'))['entryId__max']
        entryId = int(last_entryId) + 1 if last_entryId else 1001
        con_id = str(entryId)

        vendorName = request.POST.get('vendor')
        vendorCompany = request.POST.get('vendorcompany')
        receivedBy = request.POST.get('employee')
        date = request.POST.get('date')

        # Use array-based inputs
        machines = request.POST.getlist('machine[]')
        spareParts = request.POST.getlist('sparetpart[]')
        sparePartNos = request.POST.getlist('sparetpartNo[]')
        manufacturers = request.POST.getlist('manufacturer[]')
        rates = request.POST.getlist('rate[]')
        quantities = request.POST.getlist('quantity[]')
        issuedQuantities = request.POST.getlist('issuedqty[]')
        balancedQuantities = request.POST.getlist('balancedqty[]')
        pos = request.POST.getlist('po[]')

        stocks = []
        for i in range(len(machines)):
            if not machines[i] or not spareParts[i]:  # Skip invalid rows
                continue

            # Check if the sparePart and sparePartNo combination exists in the Item table
            existing_item = Item.objects.filter(
                sparePart=spareParts[i],
                sparePartNo=sparePartNos[i]
            ).first()

            if existing_item:
                # Update the existing record
                existing_item.machineName = machines[i]
                existing_item.issuedqty = F('issuedqty') + int(issuedQuantities[i])
                existing_item.save()
            else:
                # Create a new record if it doesn't exist
                Item.objects.create(
                    machineName=machines[i],
                    sparePart=spareParts[i],
                    sparePartNo=sparePartNos[i],
                    issuedqty=issuedQuantities[i]
                )

            stocks.append(Stock(
                vendorName=vendorName,
                vendorCompany=vendorCompany,
                receivedBy=receivedBy,
                date=date,
                machineName=machines[i],
                sparePart=spareParts[i],
                sparePartNo=sparePartNos[i],
                manufacturerName=manufacturers[i],
                rate=rates[i],
                quantity=quantities[i],
                issuedqty=issuedQuantities[i],
                balanceqty=balancedQuantities[i],
                po=pos[i],
                entryId=con_id
            ))

        if stocks:
            Stock.objects.bulk_create(stocks)

        return redirect('entryHistory')

    # Context for GET request
    machine = Machine.objects.all()
    spareParts = Spareparts.objects.all()
    vendor = Vendor.objects.all()
    employee = Employee.objects.all()

    return render(request, 'entryHistory.html', {
        'machine': machine,
        'spareParts': spareParts,
        'vendor': vendor,
        'employee': employee
    })


def get_vendor_details(request):
    name = request.GET.get('name', '')
    if name:
        consignor = Vendor.objects.filter(vendorName=name).first()
        if consignor:
            data = {
                'companyName': consignor.companyName,
            }
        else:
            data = {}
    else:
        data = {}

    return JsonResponse(data)

def get_spare_details(request):
    name = request.GET.get('name', '')
    if name:
        consignor = Spareparts.objects.filter(sparepart=name).first()
        if consignor:
            data = {
                'sparepartNo': consignor.sparepartNo,
            }
        else:
            data = {}
    else:
        data = {}

    return JsonResponse(data)
from datetime import datetime

def entryHistoryList(request):
    # Fetch date filter from request
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Filter entries by date if provided
    entries = Stock.objects.all()
    if from_date:
        entries = entries.filter(date__gte=datetime.strptime(from_date, "%Y-%m-%d").date())
    if to_date:
        entries = entries.filter(date__lte=datetime.strptime(to_date, "%Y-%m-%d").date())

    # Group entries by entryId and calculate aggregate fields
    entries_summary = {}
    for entry in entries:
        entry_id = entry.entryId
        if entry_id not in entries_summary:
            # Initialize summary for each entryId
            entries_summary[entry_id] = {
                'date': entry.date,
                'machine_name': entry.machineName,
                'spare_parts': [],
                'total_issued_qty': 0,
            }

        # Add spare part details for each entry
        entries_summary[entry_id]['spare_parts'].append({
            'machineName': entry.machineName,
            'sparePart': entry.sparePart,
            'issuedQty': entry.issuedqty,
        })

        # Update aggregate totals for issuedQty
        entries_summary[entry_id]['total_issued_qty'] += entry.issuedqty


    return render(request,'entryHistoryList.html',{'entries_summary':entries_summary})


def edit_entry(request, entry_id):
    # Fetch vendor and spare part details for the specified entry
    vendordeatils = Stock.objects.filter(entryId=entry_id).values('vendorName', 'vendorCompany', 'receivedBy').first()  # Use .first() to get a single result
    spare_part_details = Stock.objects.filter(entryId=entry_id).values(
        'vendorName', 'vendorCompany', 'receivedBy', 'machineName', 'sparePart',
        'sparePartNo', 'manufacturerName', 'rate', 'quantity', 'issuedqty',
        'balanceqty', 'po'
    )

    if request.method == 'POST':
        # Handle vendor form submission
        vendor_name = request.POST.get('vendor')
        vendor_company = request.POST.get('vendorcompany')
        received_by = request.POST.get('employee')

        # Update vendor details in the Stock table (assuming only one entry per vendor)
        Stock.objects.filter(entryId=entry_id).update(
            vendorName=vendor_name, vendorCompany=vendor_company, receivedBy=received_by
        )

        # Iterate over the spare part details and update each spare part entry
        for i in range(len(request.POST.getlist('machine'))):
            machine = request.POST.getlist('machine')[i]
            spare_part = request.POST.getlist('sparetpart')[i]
            spare_part_no = request.POST.getlist('sparetpartNo')[i]
            manufacturer = request.POST.getlist('manufacturer')[i]
            rate = request.POST.getlist('rate')[i]
            quantity = request.POST.getlist('quantity')[i]
            issuedqty = request.POST.getlist('issuedqty')[i]
            balanceqty = request.POST.getlist('balancedqty')[i]
            po = request.POST.getlist('po')[i]

            # Update or create entries in Stock for each spare part
            Stock.objects.update_or_create(
                entryId=entry_id, sparePart=spare_part, defaults={
                    'machineName': machine, 'sparePartNo': spare_part_no,
                    'manufacturerName': manufacturer, 'rate': rate,
                    'quantity': quantity, 'issuedqty': issuedqty,
                    'balanceqty': balanceqty, 'po': po
                }
            )

        # Redirect to entry history list after updating the details
        return redirect('entryHistoryList')

    machine = Machine.objects.all()
    spareParts = Spareparts.objects.all()
    vendor = Vendor.objects.all()
    employee = Employee.objects.all()

    return render(request, 'edit_entry.html', {
        'entry_id': entry_id,
        'spare_part_details': spare_part_details,
        'vendordeatils': vendordeatils,
        'machine':machine,
        'spareParts':spareParts,
        'vendor':vendor,
        'employee':employee

    })

logger = logging.getLogger(__name__)


def stockToDepartment(request):
    """Render the main template with all items and handle form submission."""
    stock = Spareparts.objects.all()
    department = Department.objects.all()
    machine = Machine.objects.all()
    error_message = None  # Initialize error_message

    if request.method == "POST":
        try:
            now = datetime.now()
            con_date = now.strftime("%Y-%m-%d")
            sparetpart = request.POST.get('sparetpart')
            machine = request.POST.get('machine')
            part_no = request.POST.get('sparetpartNo')
            issuedqty = int(request.POST.get('quantity', 0))
            department = request.POST.get('department')

            # Check for missing fields
            if not all([sparetpart, part_no, issuedqty, department]):
                error_message = "All fields are required."
                return render(request, "stockToDepartment.html", {
                    "stock": stock,
                    "department": department,
                    'machine': machine,
                    'error_message': error_message
                })

            # Check for item existence in Godown
            godown_items = Item.objects.filter(sparePart=sparetpart, sparePartNo=part_no)
            logger.debug(f"Found {godown_items.count()} items in the godown")

            if godown_items.exists():
                godown_item = godown_items.first()

                # Check if there is enough quantity in the godown
                if godown_item.issuedqty >= issuedqty:
                    # Update the godown item
                    godown_item.issuedqty -= issuedqty
                    godown_item.save()

                    # Check if the record already exists in Deptstock table
                    deptstock_item = Deptstock.objects.filter(
                        sparePart=sparetpart,
                        sparePartNo=part_no,
                        department=department
                    ).first()

                    if deptstock_item:
                        # If the record exists, update the quantity and date
                        deptstock_item.qty += issuedqty
                        deptstock_item.date = con_date
                        deptstock_item.save()
                    else:
                        # If the record doesn't exist, create a new entry
                        Deptstock.objects.create(
                            machineName=machine,
                            sparePart=sparetpart,
                            sparePartNo=part_no,
                            qty=issuedqty,
                            department=department,
                            date=con_date
                        )

                    # Save data to StocktoDept table
                    godown_to_branch = StocktoDept(
                        machineName=machine,
                        sparePart=sparetpart,
                        sparePartNo=part_no,
                        qty=issuedqty,
                        department=department,
                        date=con_date
                    )
                    godown_to_branch.save()

                    return redirect('stockToDepartment')  # Redirect to the same page for new form submission

                else:
                    error_message = "Insufficient quantity in Godown!"
            else:
                error_message = "Item not found in Godown!"
        except Exception as e:
            logger.error("Error processing form data: %s", e)
            error_message = "Server error."

        # If there is an error, pass it to the template
        return render(request, "stockToDepartment.html", {
            "stock": stock,
            "department": department,
            'machine': machine,
            'error_message': error_message
        })

    return render(request, "stockToDepartment.html", {
        "stock": stock,
        "department": department,
        'machine': machine
    })

def stockToDepartmentList(request):
    stock = StocktoDept.objects.all()
    return render(request,'stockToDepartmentList.html',{'stock':stock})

def sparePartStock(request):
    spartpart = Spareparts.objects.all()  # Get all spare parts
    spare = Stock.objects.all()  # Get all stock records

    if request.method == "POST":
        sparetpart = request.POST.get('sparetpart')

        if sparetpart:
            # Filter the stock records based on the selected spare part name
            spare = spare.filter(sparePart=sparetpart)
            # Group the stock by spare part and calculate the total quantity
            grouped_stock = spare.values('sparePart').annotate(total_stock=Sum('quantity'))
        else:
            # If no spare part is selected, show all stock grouped by spare part
            grouped_stock = spare.values('sparePart').annotate(total_stock=Sum('quantity'))
    else:
        # Default: show all stock grouped by spare part
        grouped_stock = spare.values('sparePart').annotate(total_stock=Sum('quantity'))

    return render(request, 'sparePartStock.html', {
        'spartpart': spartpart,
        'grouped_stock': grouped_stock,
    })
from django.utils.dateparse import parse_date

def viewSpare(request, name):
    # Capture the 'from_date' and 'to_date' from the POST request
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')

    # Convert the dates to proper format if they exist
    if from_date:
        from_date = parse_date(from_date)
    if to_date:
        to_date = parse_date(to_date)

    # Get all stock items that match the spare part name (returns a QuerySet)
    spare = Stock.objects.filter(sparePart=name)

    # If dates are provided, filter the spare items by the date range
    if from_date and to_date:
        spare = spare.filter(date__range=[from_date, to_date])
    elif from_date:
        spare = spare.filter(date__gte=from_date)
    elif to_date:
        spare = spare.filter(date__lte=to_date)

    # Calculate the total issued quantity (sum of issuedqty)
    total_issued_qty = spare.aggregate(Sum('issuedqty'))['issuedqty__sum'] or 0  # Default to 0 if no results

    # Handle the case where there might be no matching spare parts
    if spare:
        sparepart = spare.first().sparePartNo  # Access sparePartNo from the first stock item (or loop over if needed)
        image = Spareparts.objects.get(sparepartNo=sparepart)  # Get the related Spareparts object
    else:
        spare = None  # If no spare part is found
        image = None

    # Pass the spare items and total issued quantity to the template
    return render(request, 'viewSpare.html', {
        'spare': spare,
        'image': image,
        'total_issued_qty': total_issued_qty,
        'from_date': from_date,
        'to_date': to_date,
    })

logger = logging.getLogger(__name__)

def departmentTodepartment(request):
    """Render the main template with all items and handle form submission."""
    stock = Spareparts.objects.all()
    department = Department.objects.all()
    machine = Machine.objects.all()
    error_message = None  # Initialize error_message

    if request.method == "POST":
        try:
            now = datetime.now()
            con_date = now.strftime("%Y-%m-%d")
            sparetpart = request.POST.get('sparetpart')
            machine = request.POST.get('machine')
            part_no = request.POST.get('sparetpartNo')
            qty = int(request.POST.get('quantity', 0))
            fromdepartment = request.POST.get('fromdepartment')
            todepartment = request.POST.get('todepartment')

            # Log the received form data
            logger.debug(f"Form data received: sparetpart={sparetpart}, part_no={part_no}, qty={qty}, "
                         f"fromdepartment={fromdepartment}, todepartment={todepartment}, machine={machine}")

            # Check if any required fields are missing
            if not all([sparetpart, part_no, qty, fromdepartment, todepartment]):
                error_message = "All fields are required."
                logger.error(f"Error: {error_message}. Missing fields: "
                             f"sparetpart={sparetpart}, part_no={part_no}, qty={qty}, "
                             f"fromdepartment={fromdepartment}, todepartment={todepartment}")
                return render(request, "departmentTodepartment.html", {
                    "stock": stock,
                    "department": department,
                    'machine': machine,
                    'error_message': error_message
                })

            # Check for the item in the fromdepartment
            godown_items = Deptstock.objects.filter(sparePart=sparetpart, sparePartNo=part_no, department=fromdepartment)
            logger.debug(f"Found {godown_items.count()} items in the fromdepartment")

            if godown_items.exists():
                godown_item = godown_items.first()

                # Ensure there's enough stock in the fromdepartment
                if godown_item.qty >= qty:
                    godown_item.qty -= qty
                    godown_item.save()

                    # Check if the item already exists in the todepartment
                    to_dept_item = Deptstock.objects.filter(sparePart=sparetpart, sparePartNo=part_no, department=todepartment).first()

                    if to_dept_item:
                        # If the record exists in todepartment, update it
                        to_dept_item.qty += qty
                        to_dept_item.date = con_date
                        to_dept_item.save()
                    else:
                        # If no record exists, create a new entry in the todepartment
                        Deptstock.objects.create(
                            sparePart=sparetpart,
                            sparePartNo=part_no,
                            qty=qty,
                            department=todepartment,
                            date=con_date,
                            machineName=machine
                        )

                    # Record the transfer in DepttoDept table
                    godown_to_branch = DepttoDept(
                        machineName=machine,
                        sparePart=sparetpart,
                        sparePartNo=part_no,
                        qty=qty,
                        fromdepartment=fromdepartment,
                        todepartment=todepartment,
                        date=con_date
                    )
                    godown_to_branch.save()

                    return redirect('departmentTodepartment')  # Redirect to refresh the page or target another view

                else:
                    error_message = "Insufficient quantity in the fromdepartment!"
                    logger.error(f"Error: {error_message}. Available qty: {godown_item.qty}, requested qty: {qty}")

            else:
                error_message = "Item not found in the fromdepartment!"
                logger.error(f"Error: {error_message}. SparePart: {sparetpart}, SparePartNo: {part_no}, FromDepartment: {fromdepartment}")

        except Exception as e:
            logger.error("Error processing form data: %s", e)
            error_message = "Server error."

        # If there is an error, pass it to the template
        return render(request, "departmentTodepartment.html", {
            "stock": stock,
            "department": department,
            'machine': machine,
            'error_message': error_message
        })

    return render(request, "departmentTodepartment.html", {
        "stock": stock,
        "department": department,
        'machine': machine
    })

def deptTodeptList(request):
    stock = DepttoDept.objects.all()
    return render(request,'deptTodeptList.html',{'stock':stock})

def deptStock(request):
    stock = Deptstock.objects.all()
    return render(request,'deptStock.html',{'stock':stock})